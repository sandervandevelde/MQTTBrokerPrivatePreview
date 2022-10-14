#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

ns_name="mqtt-sample4-${ns_name_suffix}"
resource_prefix="${ns_id_prefix}/${ns_name}"
gw_url="${ns_name}.centraluseuap-1.ts.eventgrid.azure.net"

eg_topic_name="eg-sample-topic-${az_region}"
eg_topic_id="/subscriptions/${sub_id}/resourcegroups/${rg_name}/providers/Microsoft.EventGrid/topics/${eg_topic_name}"

pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s4-vehicle1
popd

echo "Setting up EventGrid topic."
az eventgrid topic create -g ${rg_name} --name ${eg_topic_name} -l ${az_region} --input-schema cloudeventschemav1_0 
az role assignment create --assignee ${ad_username} --role "EventGrid Data Sender" --scope "${eg_topic_id}"
az provider register --namespace Microsoft.EventGrid
echo "EventGrid topic created."

echo "Updating namespace resource file with EventGrid topic"
escaped_eg_topic_id=$(printf '%s\n' "$eg_topic_id" | sed -e 's/[\/&]/\\&/g')
sed -i "s/<<eg-topic-id>>/${escaped_eg_topic_id}/" ./resources/NS_Scenario4.json
echo "Namespace resource file updated."

echo "Uploading ${ns_name} resources..."

az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario4.json

az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json

az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/vehicle-publish --api-version 2022-10-15-preview --properties @./resources/TS_vehicle-publish.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s4-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json

az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicle --api-version 2022-10-15-preview --properties @./resources/CG_vehicle.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicle-publisher --api-version 2022-10-15-preview --properties @./resources/PB_vehicle-publisher.json

echo "Resources uploaded."

echo "Run the following in all shell windows before running python scripts:"
echo "export gw_url=${gw_url}"