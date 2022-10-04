#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

ns_name="Scenario0"
sub_id="bdf55cdd-8dab-4cf4-9b2f-c21e8a780472"
rg_name="slbojanic-rg"
base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces/${ns_name}"

# WARNING: do this only once
az cloud register --name Dogfood --endpoint-active-directory-resource-id  https://management.core.windows.net/ --endpoint-resource-manager https://api-dogfood.resources.windows-int.net/ --endpoint-active-directory  https://login.windows-ppe.net/ --endpoint-active-directory-graph-resource-id https://graph.ppe.windows.net/

az cloud set --name Dogfood
az login

pushd ../cert-gen
./certGen.sh create_root_and_intermediate
./certGen.sh create_leaf_certificate_from_intermediate pub_client
./certGen.sh create_leaf_certificate_from_intermediate sub_client

#openssl x509 -noout -text -in "certs/pub_client.cert.pem"
popd

az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario0.json

az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CACertificate.json

az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/hello --api-version 2022-10-15-preview --properties @./resources/TS_hello.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/pub_client --api-version 2022-10-15-preview --properties @./resources/C_pub_client.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/sub_client --api-version 2022-10-15-preview --properties @./resources/C_sub_client.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/sub_hello --api-version 2022-10-15-preview --properties @./resources/PB_subscriber.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/pub_hello --api-version 2022-10-15-preview --properties @./resources/PB_publisher.json
