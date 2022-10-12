# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)

client_id = "pub-client"
gw_url = os.environ["gw_url"]

topic = "samples/topic"
payload = {"latitude": 47.63962283908785, "longitude": -122.12718926895407}

cert_path = "../cert-gen/certs/pub-client.cert.pem"
cert_key_path = "../cert-gen/certs/pub-client.key.pem"

##################################
# CREATE CLIENT
##################################

client = PahoClient.create_from_x509_certificate(client_id, cert_path, cert_key_path, "1234", gw_url)

##################################
# CONNECT
##################################

print("Connecting to {}".format(client.auth.device_id))
client.start_connect()

if not client.connection_status.wait_for_connected(timeout=20):
    print("failed to connect.  exiting")
    sys.exit(1)
print("Connected")
print()

##################################
# PUBLISH
##################################

print("Publishing to {} at QOS=1".format(topic))
(rc, mid) = client.publish(topic, json.dumps(payload), qos=1)
print("Publish returned rc={}: {}".format(rc, PahoClient.error_string(rc)))

print("Waiting for PUBACK for mid={}".format(mid))
if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
    print("PUBACK received")
else:
    print("PUBACK not received within 20 seconds")
print()

##################################
# DISCONNECT
##################################

print("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()
