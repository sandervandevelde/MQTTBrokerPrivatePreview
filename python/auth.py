# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import abc
import threading
import time
import logging
import ssl
import hmac
import hashlib
import base64
from typing import Any, Callable, Union, Dict
from six.moves import urllib

logger = logging.getLogger(__name__)

new_password_available_handler = Callable[[], None]

API_VERSION = "2021-06-30-preview"

# Defult expiration period, in seconds, of any passwords (SAS tokens) created by this code
DEFAULT_PASSWORD_RENEWAL_INTERVAL = 3600

# Number of seconds before a password (SAS token) expires that this code will create a new password.
DEFAULT_PASSWORD_RENEWAL_MARGIN = 300


def sign_password(base64_key: str, payload_to_sign: Union[str, bytes]) -> bytes:
    # assume base64_key is a string.
    decoded_key = base64.b64decode(base64_key)

    try:
        payload_to_sign = payload_to_sign.encode("utf-8")  # type: ignore
    except AttributeError:
        # If byte string, no need to encode
        pass

    return base64.b64encode(
        hmac.HMAC(
            key=decoded_key,
            msg=payload_to_sign,  # type: ignore
            digestmod=hashlib.sha256,
        ).digest()
    )


def encode_dict(obj: Dict[str, str]) -> str:
    return "&".join(
        [
            "{}={}".format(
                urllib.parse.quote(k, safe=""), urllib.parse.quote(v, safe="")
            )
            for k, v in obj.items()
        ]
    )


class BaseAuth(abc.ABC):
    def __init__(self) -> None:
        self.device_id = ""
        self.module_id = ""
        self.port = 8883
        self.gateway_host_name = ""
        self.hub_host_name = ""
        self.dtmi = ""
        self.product_info = ""
        self.server_verification_cert: str = None

    @property
    @abc.abstractmethod
    def password(self) -> bytes:
        """
        The password to pass in the body of MQTT CONNECT packet.
        """
        pass

    def get_base_connect_props(self) -> Dict[str, str]:
        """
        Get properties for connect packet
        """
        props = {
            "h": self.hub_host_name,
            "did": self.device_id,
            "av": API_VERSION,
        }

        if self.module_id:
            props["mid"] = self.module_id

        if self.dtmi:
            props["dtmi"] = self.dtmi

        if self.product_info:
            props["ca"] = self.product_info

        return props

    @property
    @abc.abstractmethod
    def username(self) -> str:
        """
        Value to be sent in the MQTT `username` field.
        """
        pass

    @property
    def client_id(self) -> str:
        """
        Value to be sent in the MQTT `client_id` field.
        """
        if self.module_id:
            return "{}/{}".format(self.device_id, self.module_id)
        else:
            return self.device_id

    @property
    def hostname(self) -> str:
        """
        host to connect to.  This may be the name of the IoTHub instance, or, in the case of a
        gateway, it may be the name of the gateway instance.
        """
        if self.gateway_host_name:
            return self.gateway_host_name
        else:
            return self.hub_host_name

    def create_tls_context(self) -> ssl.SSLContext:
        """
        Create an SSLContext object based on this object.

        :returns: SSLContext object which can be used to secure the TLS connection.
        """
        ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
        if self.server_verification_cert:
            ssl_context.load_verify_locations(
                cadata=self.server_verification_cert
            )
        else:
            ssl_context.load_default_certs()

        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.check_hostname = True

        return ssl_context


class SymmetricKeyAuth(BaseAuth):
    def __init__(self) -> None:
        super(SymmetricKeyAuth, self).__init__()
        self.password_creation_time = 0
        self.password_expiry_time = 0
        self.shared_access_key: str = None
        self.shared_access_key_name: str = None

    @property
    def password(self) -> bytes:
        """
        The password to pass in the body of MQTT CONNECT packet.
        """
        ss = "{host_name}\n{identity}\n{sas_policy}\n{sas_at}\n{sas_expiry}\n".format(
            host_name=self.hub_host_name,
            identity=self.client_id,
            sas_policy=self.shared_access_key_name or "",
            sas_at=self.password_creation_time * 1000,
            sas_expiry=self.password_expiry_time * 1000,
        )
        return sign_password(self.shared_access_key, ss)

    @property
    def username(self) -> str:
        """
        Value to be sent in the MQTT `username` field.
        """
        props = self.get_base_connect_props()
        props["am"] = "SASb64"
        props["se"] = str(self.password_expiry_time * 1000)
        props["sa"] = str(self.password_creation_time * 1000)

        if self.shared_access_key_name:
            props["sp"] = self.shared_access_key_name

        # TOOD: when we test this, we want to verify the characters in the spec
        return encode_dict(props)

    def update_expiry(self) -> None:
        """
        Update the expiry of for the generated password.  This causes the values returned for
        the `username` and `password` properties to be updated.
        """
        self.password_creation_time = int(time.time())
        self.password_expiry_time = int(
            self.password_creation_time + DEFAULT_PASSWORD_RENEWAL_INTERVAL
        )

    @classmethod
    def create_from_connection_string(cls, connection_string: str) -> Any:
        """
        create a new auth object from a connection string

        :param str connection_string: Connection string to create auth object for

        :returns: SymmetricKeyAuth object created by this function.
        """
        obj = cls()
        obj._initialize(connection_string)
        return obj

    def _initialize(self, connection_string: str) -> None:
        """
        Helper function to initialize a newly created auth object.
        """
        cs_args = connection_string.split(";")
        cs_dict = dict(arg.split("=", 1) for arg in cs_args)  # type: ignore

        self.hub_host_name = cs_dict["HostName"]
        self.device_id = cs_dict["DeviceId"]
        self.module_id = cs_dict.get("ModuleId", None)
        self.gateway_host_name = cs_dict.get("GatewayHostName", None)
        self.shared_access_key = cs_dict["SharedAccessKey"]

        self.update_expiry()


class X509Auth(BaseAuth):
    def __init__(self) -> None:
        super(X509Auth, self).__init__()
        self.certificate_filename: str = None
        self.key_filename: str = None
        self.pass_phrase: str = None

    @property
    def password(self) -> bytes:
        """
        The password to pass in the body of MQTT CONNECT packet.
        """
        pass

    @property
    def username(self) -> str:
        """
        Value to be sent in the MQTT `username` field.
        """
        props = self.get_base_connect_props()
        props["am"] = "X509"

        return encode_dict(props)

    @classmethod
    def create_from_x509_certificate(
        cls,
        host_name: str,
        device_id: str,
        certificate_filename: str,
        module_id: str = None,
        key_filename: str = None,
        pass_phrase: str = None,
        gateway_host_name: str = None,
    ) -> Any:
        """
        create a new auth object from a connection string

        :param hostname: Name of the IoTHub host
        :param gateway_hostname: Name of the protocol gateway or IoTEdge instance
        :param device_id: deviceId for the IoTHub device or module
        :param module_id: moduleId for teh IoTHub module
        :param cert_filename: The file path to contents of the certificate (or certificate chain)
            used to authenticate the device.
        :param key_filename: The file path to the key associated with the certificate.
        :param pass_phrase: (optional) The pass_phrase used to encode the key file.

        :returns: X509Auth object created by this function.
        """
        obj = cls()
        obj._initialize(
            host_name=host_name,
            device_id=device_id,
            certificate_filename=certificate_filename,
            module_id=module_id,
            key_filename=key_filename,
            pass_phrase=pass_phrase,
            gateway_host_name=gateway_host_name,
        )
        return obj

    def _initialize(
        self,
        host_name: str,
        device_id: str,
        certificate_filename: str,
        module_id: str,
        key_filename: str,
        pass_phrase: str,
        gateway_host_name: str,
    ) -> None:
        """
        Helper function to initialize a newly created auth object.
        """
        self.hub_host_name = host_name
        self.device_id = device_id
        self.module_id = module_id
        self.gateway_host_name = gateway_host_name

        self.certificate_filename = certificate_filename
        self.key_filename = key_filename
        self.pass_phrase = pass_phrase

    def create_tls_context(self) -> ssl.SSLContext:
        """
        Create an SSLContext object based on this object.

        :returns: SSLContext object which can be used to secure the TLS connection.
        """
        context = super(X509Auth, self).create_tls_context()

        context.load_cert_chain(
            self.certificate_filename, self.key_filename, self.pass_phrase
        )

        return context


class PasswordRenewalTimer(object):
    """
    Helper object used to set up automatic password renewal timers and events.
    """

    def __init__(self, auth: SymmetricKeyAuth) -> None:
        self.auth = auth
        self.password_renewal_timer: threading.Timer = None
        self.on_new_password_available: new_password_available_handler = None

    @property
    def password_renewal_time(self) -> int:
        """
        The Unix epoch time when the password should be renewed.  This is typically
        some amount of time before the token expires.  That amount of time is known
        as the "token renewal margin"
        """
        return self.auth.password_expiry_time - DEFAULT_PASSWORD_RENEWAL_MARGIN

    @property
    def password_ready_to_renew(self) -> bool:
        """
        True if the current password is "ready to renew", meaning the current time is
        after the password's renewal time.
        """
        return time.time() > self.password_renewal_time

    @property
    def seconds_until_password_renewal(self) -> int:
        """
        Number of seconds before the current password needs to be removed.
        """
        return max(0, self.password_renewal_time - int(time.time()))

    def cancel_password_renewal_timer(self) -> None:
        """
        Cancel the running timer which is set to fire when the current password
        needs to be renewed.
        """
        if self.password_renewal_timer:
            self.password_renewal_timer.cancel()
            self.password_renewal_timer = None

    def set_password_renewal_timer(
        self, on_new_password_available: new_password_available_handler = None
    ) -> None:
        """
        Set a timer which renews the current password before it expires and calls
        the supplied handler after the renewal is complete.  The supplied handler
        is responsible for re-authorizing using the new password and setting up a new
        timer by calling `set_password_renewal_timer` again.

        :param function on_new_password_available: Handler function which gets called after
            the password is renewed.  This function is responsible for calling
            `set_password_renewal_timer` in order to schedule subsequent renewals.
        """

        # If there is an old renewal timer, cancel it
        self.cancel_password_renewal_timer()
        self.on_new_password_available = on_new_password_available

        # Set a new timer.
        seconds_until_renewal = self.seconds_until_password_renewal
        self.password_renewal_timer = threading.Timer(
            seconds_until_renewal, self.renew_and_reconnect
        )
        self.password_renewal_timer.daemon = True
        self.password_renewal_timer.start()

        logger.info(
            "Password renewal timer set for {} seconds in the future, at approximately {}".format(
                seconds_until_renewal, self.auth.password_expiry_time
            )
        )

    def renew_and_reconnect(self) -> None:
        """
        Renew authorization. This  causes a new password string to be generated and the
            `on_new_password_available` function to be called.
        """
        logger.info("Renewing password and reconnecting")

        self.cancel_password_renewal_timer()

        self.auth.update_expiry()

        if self.on_new_password_available:
            self.on_new_password_available()
