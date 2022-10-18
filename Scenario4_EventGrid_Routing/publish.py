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

client_id = "s4-vehicle1"
cert_path = "../cert-gen/certs/s4-vehicle1.cert.pem"
cert_key_path = "../cert-gen/certs/s4-vehicle1.key.pem"

##################################
# CREATE CLIENT
##################################

client = PahoClient.create_from_x509_certificate(
    client_id, cert_path, cert_key_path, "1234", gw_url
)

##################################
# CONNECT
##################################

client.print_msg("Starting connection")
client.start_connect()
if not client.connection_status.wait_for_connected(timeout=20):
    client.print_msg("Failed to connect. Exiting")
    sys.exit(1)
client.print_msg("Connected")
print()

##################################
# PUBLISH
##################################

topic = "vehicles/{}/GPS/position".format(client.auth.device_id)

for i in range(1, 20):
    payload = {
        "latitude": 47.63962283908785 - i,
        "longitude": -122.12718926895407,
        "index": i,
    }

    client.print_msg(
        "Publishing to {} at QOS=1: {}".format(topic, payload)
    )
    (rc, mid) = client.publish(topic, json.dumps(payload), qos=1)
    client.print_msg(
        "Publish returned rc={}: {}".format(rc, PahoClient.error_string(rc))
    )

    client.print_msg("Waiting for PUBACK for mid={}".format(mid))
    if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
        client.print_msg("PUBACK received")
    else:
        client.print_msg("PUBACK not received within 20 seconds")
    print()

    time.sleep(0.5)

##################################
# DISCONNECT
##################################

client.print_msg("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()