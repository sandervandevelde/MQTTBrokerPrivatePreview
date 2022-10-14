# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
import uuid
import time
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)

gw_url = os.environ["gw_url"]

vehicle_device_id = "s3-vehicle1"

mobile_device_id = "s3-mobile1"
cert_path = "../cert-gen/certs/s3-mobile1.cert.pem"
cert_key_path = "../cert-gen/certs/s3-mobile1.key.pem"

##################################
# CREATE CLIENTS
##################################

client = PahoClient.create_from_x509_certificate(
    mobile_device_id, cert_path, cert_key_path, "1234", gw_url
)


topic = "vehicles/unlock/req/{}/{}".format(vehicle_device_id, client.auth.device_id)
topic_filter = "vehicles/unlock/res/{}/#".format(client.auth.device_id)

##################################
# CONNECT
##################################

print("{}: Connecting".format(client.auth.device_id))
client.start_connect()
if not client.connection_status.wait_for_connected(timeout=20):
    print("{}: Connection failed.  Exiting.".format(client.auth.device_id))
    sys.exit(1)
print("{}: Connected".format(client.auth.device_id))
print()
##################################
# SUBSCRIBE
##################################

qos = 1
print(
    "{}: Subscribing to {} at qos {}".format(client.auth.device_id, topic_filter, qos)
)
(rc, mid) = client.subscribe(topic_filter, qos)

ack_result = client.incoming_subacks.wait_for_ack(mid, timeout=20)
if not ack_result:
    print("{}: SUBACK not received within 20 seconds".format(client.auth.device_id))
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
elif ack_result[0] == -1:
    print("{}: Subscription was rejected".format(client.auth.device_id))
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
else:
    print(
        "{}: Subscription was granted with qos {}".format(
            client.auth.device_id, ack_result[0]
        )
    )
print()

##################################
# PUBLISH
##################################

command_id = str(uuid.uuid4())
payload = {
    "command": "unlock",
    "commandId": command_id,
    "requestorId": client.auth.device_id,
    "authorization": "pretty pretty please",
    "credentials": "with a cherry on top",
}


print(
    "{}: Publishing to {} at QOS {}: {}".format(
        client.auth.device_id, topic, qos, payload
    )
)
(rc, mid) = client.publish(topic, json.dumps(payload), qos=qos)
print(
    "{}: Publish returned rc={}: {}".format(
        client.auth.device_id, rc, PahoClient.error_string(rc)
    )
)

print("{}: Waiting for PUBACK for mid={}".format(client.auth.device_id, mid))
if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
    print("{}: PUBACK received".format(client.auth.device_id))
else:
    print("{}: PUBACK not received within 20 seconds".format(client.auth.device_id))
print()

##################################
# LISTEN
##################################

time_to_listen_in_seconds = 60
end_time = time.time() + time_to_listen_in_seconds

while time.time() <= end_time:
    remaining_time = end_time - time.time()
    print(
        "{}: listening for response for {} more seconds".format(
            client.auth.device_id, remaining_time
        )
    )

    message = client.incoming_messages.pop_next_message(timeout=remaining_time)
    if message:
        payload_object = json.loads(message.payload)
        print(
            "{}: Message for UNLOCKED received on topic {}: {}".format(
                client.auth.device_id, message.topic, payload_object
            )
        )
        if payload_object["commandId"] == command_id:
            print(
                "{}: response received.  Result={}".format(
                    client.auth.device_id, payload_object["result"]
                )
            )
            break
        else:
            print("{}: unknown response.  Ignoring".format(client.auth.device_id))

print()

##################################
# DISCONNECT
##################################

print("{}: Disconnecting".format(client.auth.device_id))
client.disconnect()
client.connection_status.wait_for_disconnected()