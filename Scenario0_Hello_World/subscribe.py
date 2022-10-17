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

client_id = "sub-client"
gw_url = os.environ["gw_url"]

topic_filter = "samples/#"

cert_path = "../cert-gen/certs/sub-client.cert.pem"
cert_key_path = "../cert-gen/certs/sub-client.key.pem"

##################################
# CREATE CLIENT
##################################

client = PahoClient.create_from_x509_certificate(
    client_id, cert_path, cert_key_path, "1234", gw_url, clean_session=True
)

##################################
# CONNECT
##################################

client.print_msg("Connecting...")
client.start_connect()
if not client.connection_status.wait_for_connected(timeout=20):
    client.print_msg("Failed to connect. Exiting")
    sys.exit(1)
client.print_msg("Connected")
print()

##################################
# SUBSCRIBE
##################################

qos = 1
client.print_msg("Subscribing to {} at qos {}".format(topic_filter, qos))
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
    client.print_msg("Subscription was granted with qos {}".format(ack_result[0]))
print()

##################################
# LISTEN
##################################

time_to_listen_in_seconds = 300
end_time = time.time() + time_to_listen_in_seconds

while time.time() <= end_time:
    remaining_time = end_time - time.time()
    client.print_msg("{}: Waiting for messages for {} more seconds".format(time.time(), remaining_time))

    message = client.incoming_messages.pop_next_message(timeout=remaining_time)
    if message:
        client.print_msg("Message received on topic {}".format(message.topic))
        payload_object = json.loads(message.payload)
        client.print_msg("Payload: {}".format(payload_object))
print()

##################################
# DISCONNECT
##################################

time.sleep(1)
client.print_msg("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()
