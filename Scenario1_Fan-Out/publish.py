# Copyright (c) Microsoft Corporation. All rights reserved.
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

client_id = "s1-fleet-mgr"
gw_url = os.environ["gw_url"]

cert_path = "../cert-gen/certs/s1-fleet-mgr.cert.pem"
cert_key_path = "../cert-gen/certs/s1-fleet-mgr.key.pem"

##################################
# CREATE CLIENT
##################################

client = PahoClient.create_from_x509_certificate(client_id, cert_path, cert_key_path, "1234", gw_url)

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

topic = "fleet/alerts/weather/alert1"
payload = {
    "message": "The national weather service has issued a tornado watch for Milwaukee County until 8 PM tonight"
}

client.print_msg("Publishing to {} at QOS=1: {}".format(topic, payload))
(rc, mid) = client.publish(topic, json.dumps(payload), qos=1)
client.print_msg(
    "Publish returned rc={}: {}".format(rc, PahoClient.error_string(rc))
)

timeout_sec = 60
client.print_msg("Waiting for PUBACK for mid={}".format(mid))
if client.incoming_pubacks.wait_for_ack(mid, timeout=timeout_sec):
    client.print_msg("PUBACK received")
else:
    client.print_msg("PUBACK not received within {} seconds".format(timeout_sec))
print()

##################################
# DISCONNECT
##################################

time.sleep(2)
client.print_msg("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()