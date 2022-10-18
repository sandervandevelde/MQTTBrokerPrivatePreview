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

client.print_msg("Connecting")
client.start_connect()
if not client.connection_status.wait_for_connected(timeout=20):
    client.print_msg("Connection failed. Exiting.")
    sys.exit(1)
client.print_msg("Connected")
print()
##################################
# SUBSCRIBE
##################################

qos = 1
client.print_msg(
    "Subscribing to {} at qos {}".format(topic_filter, qos)
)
(rc, mid) = client.subscribe(topic_filter, qos)

ack_result = client.incoming_subacks.wait_for_ack(mid, timeout=20)
if not ack_result:
    client.print_msg("SUBACK not received within 20 seconds")
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
elif ack_result[0] == -1:
    client.print_msg("Subscription was rejected")
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
else:
    client.print_msg(
        "Subscription was granted with qos {}".format(ack_result[0])
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


client.print_msg(
    "Publishing to {} at QOS {}: {}".format(topic, qos, payload)
)
(rc, mid) = client.publish(topic, json.dumps(payload), qos=qos)
client.print_msg(
    "Publish returned rc={}: {}".format(rc, PahoClient.error_string(rc))
)

client.print_msg("Waiting for PUBACK for mid={}".format(mid))
if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
    client.print_msg("PUBACK received")
else:
    client.print_msg("PUBACK not received within 20 seconds")
print()

##################################
# LISTEN
##################################

time_to_listen_in_seconds = 60
end_time = time.time() + time_to_listen_in_seconds

while time.time() <= end_time:
    remaining_time = end_time - time.time()
    client.print_msg(
        "listening for response for {} more seconds".format(remaining_time)
    )

    message = client.incoming_messages.pop_next_message(timeout=remaining_time)
    if message:
        payload_object = json.loads(message.payload)
        client.print_msg(
            "{}: Message for UNLOCKED received on topic {}: {}".format(
                client.auth.device_id, message.topic, payload_object
            )
        )
        if payload_object["commandId"] == command_id:
            client.print_msg(
                "response received.  Result={}".format(payload_object["result"])
            )
            break
        else:
            client.print_msg("unknown response. Ignoring")

print()

##################################
# DISCONNECT
##################################

time.sleep(2)
client.print_msg("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()