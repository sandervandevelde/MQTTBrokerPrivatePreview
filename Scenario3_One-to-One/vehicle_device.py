# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
import time
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)

gw_url = os.environ["gw_url"]

vehicle_device_id = "s3-vehicle1"
cert_path = "../cert-gen/certs/s3-vehicle1.cert.pem"
cert_key_path = "../cert-gen/certs/s3-vehicle1.key.pem"


##################################
# CREATE CLIENTS
##################################

client = PahoClient.create_from_x509_certificate(
    vehicle_device_id, cert_path, cert_key_path, "1234", gw_url
)

topic_filter = "vehicles/unlock/req/{}/#".format(client.auth.device_id)

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
        "Subscription was granted with qos {}".format(
            ack_result[0]
        )
    )
print()

##################################
# LISTEN
##################################

time_to_listen_in_seconds = 600
end_time = time.time() + time_to_listen_in_seconds

while time.time() <= end_time:
    remaining_time = end_time - time.time()
    client.print_msg(
        "listening for {} more seconds".format(remaining_time)
    )

    message = client.incoming_messages.pop_next_message(timeout=remaining_time)
    if message:
        payload_object = json.loads(message.payload)
        client.print_msg(
            "Message for UNLOCK received on topic {}: {}".format(
                message.topic, payload_object
            )
        )
        if message.topic.startswith(
            "vehicles/unlock/req/{}/".format(client.auth.device_id)
        ):
            response_payload = {
                "commandId": payload_object["commandId"],
                "result": "Success",
            }
            topic = "vehicles/unlock/res/{}/{}".format(
                payload_object["requestorId"], client.auth.device_id
            )
            client.print_msg(
                "publishing to {}: {}".format(
                    topic, response_payload
                )
            )
            (rc, mid) = client.publish(topic, json.dumps(response_payload), qos=1)
            client.print_msg(
                "Publish returned rc={}: {}".format(
                    rc, PahoClient.error_string(rc)
                )
            )
            # Not listening for puback.  Trust the transport to deliver it, but don't bother keeping track of it.
        else:
            client.print_msg("unknown request. Ignoring")
        print()


##################################
# DISCONNECT
##################################

time.sleep(2)
client.print_msg("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()