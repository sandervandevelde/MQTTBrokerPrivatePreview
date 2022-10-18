# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
import time
from concurrent.futures import ThreadPoolExecutor
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""

# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)

gw_url = os.environ["gw_url"]

client1_id = "s1-vehicle1"
cert1_path = "../cert-gen/certs/s1-vehicle1.cert.pem"
cert1_key_path = "../cert-gen/certs/s1-vehicle1.key.pem"

client2_id = "s1-vehicle2"
cert2_path = "../cert-gen/certs/s1-vehicle2.cert.pem"
cert2_key_path = "../cert-gen/certs/s1-vehicle2.key.pem"

##################################
# CREATE CLIENTS
##################################

client_1 = PahoClient.create_from_x509_certificate(client1_id, cert1_path, cert1_key_path, "1234", gw_url)

client_2 = PahoClient.create_from_x509_certificate(client2_id, cert2_path, cert2_key_path, "1234", gw_url)

all_clients = (client_1, client_2)


def listen(client: PahoClient) -> None:
    ##################################
    # CONNECT
    ##################################

    client.print_msg("Connecting...")
    client.start_connect()
    if not client.connection_status.wait_for_connected(timeout=20):
        client.print_msg("Failed to connect. Exiting")
        sys.exit(1)
    client.print_msg("Connected")

    ##################################
    # SUBSCRIBE
    ##################################

    qos = 1
    topic_filter = "fleet/alerts/#"

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
        client.print_msg(
            "Subscription was granted with qos {}".format(ack_result[0])
        )

    ##################################
    # LISTEN
    ##################################

    time_to_listen_in_seconds = 300
    end_time = time.time() + time_to_listen_in_seconds

    while time.time() <= end_time:
        remaining_time = end_time - time.time()
        client.print_msg("Waiting for messages for {} more seconds".format(remaining_time))

        message = client.incoming_messages.pop_next_message(timeout=remaining_time)
        if message:
            payload_object = json.loads(message.payload)
            client.print_msg(
                "Message received on topic {}: {}".format(message.topic, payload_object)
            )

    ##################################
    # DISCONNECT
    ##################################

    time.sleep(1)
    client.print_msg("Disconnecting")
    client.disconnect()
    client.connection_status.wait_for_disconnected()


##################################
# CREATE_THREADS
##################################

with ThreadPoolExecutor() as tp:
    for client in all_clients:
        tp.submit(listen, client)