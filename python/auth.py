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

class BaseAuth(abc.ABC):
    def __init__(self) -> None:
        self.device_id = ""
        self.port = 8883
        self.gateway_host_name = ""
        self.server_verification_cert: str = None

    @property
    def client_id(self) -> str:
        """
        Value to be sent in the MQTT `client_id` field.
        """
        return self.device_id

    @property
    def hostname(self) -> str:
        """
        host to connect to -- the name of the gateway instance.
        """
        return self.gateway_host_name

    def create_tls_context(self) -> ssl.SSLContext:
        """
        Create an SSLContext object based on this object.

        :returns: SSLContext object which can be used to secure the TLS connection.
        """
        ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)

        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.check_hostname = False

        return ssl_context


class X509Auth(BaseAuth):
    def __init__(self) -> None:
        super(X509Auth, self).__init__()
        self.certificate_filename: str = None
        self.key_filename: str = None
        self.pass_phrase: str = None

    @classmethod
    def create_from_x509_certificate(
        cls,
        device_id: str,
        certificate_filename: str,
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
            device_id=device_id,
            certificate_filename=certificate_filename,
            key_filename=key_filename,
            pass_phrase=pass_phrase,
            gateway_host_name=gateway_host_name,
        )
        return obj

    def _initialize(
        self,
        device_id: str,
        certificate_filename: str,
        key_filename: str,
        pass_phrase: str,
        gateway_host_name: str,
    ) -> None:
        """
        Helper function to initialize a newly created auth object.
        """
        self.device_id = device_id
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
