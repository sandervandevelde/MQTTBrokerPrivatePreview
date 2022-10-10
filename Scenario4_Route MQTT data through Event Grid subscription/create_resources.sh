#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

ns_name="mqtt-sample-Scenario4"
sub_id="d48566a8-2428-4a6c-8347-9675d09fb851"
rg_name="slb-rg"
base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces/${ns_name}"

pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s4-vehicle1
popd

echo "Uploading Scenario4 resources..."

az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario4.json

az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json

az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/vehicle-publish --api-version 2022-10-15-preview --properties @./resources/TS_vehicle-publish.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s3-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json

az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicle --api-version 2022-10-15-preview --properties @./resources/CG_vehicle.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicle-publisher --api-version 2022-10-15-preview --properties @./resources/PB_vehicle-publisher.json

echo "Resources uploaded."

export gw_url="mqtt-sample-scenario4.southcentralus-1.mqtt.eventgrid-int.azure.net"
echo "gw_url set to ${gw_url}"
