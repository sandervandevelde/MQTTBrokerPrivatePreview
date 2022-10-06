#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

ns_name="mqtt-sample-Scenario1"
sub_id="d48566a8-2428-4a6c-8347-9675d09fb851"
rg_name="slb-rg"
base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces/${ns_name}"

pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s1-vehicle1
./certGen.sh create_leaf_certificate_from_intermediate s1-vehicle2
./certGen.sh create_leaf_certificate_from_intermediate s1-fleet-mgr
popd

az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario1.json

az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json

az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/weather-alerts --api-version 2022-10-15-preview --properties @./resources/TS_weather-alerts.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-vehicle2 --api-version 2022-10-15-preview --properties @./resources/C_vehicle2.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-fleet-mgr --api-version 2022-10-15-preview --properties @./resources/C_fleet-mgr.json

az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/fleet-mgr --api-version 2022-10-15-preview --properties @./resources/CG_fleet-mgr.json

az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicles --api-version 2022-10-15-preview --properties @./resources/CG_vehicles.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/fleet-mgr-publisher --api-version 2022-10-15-preview --properties @./resources/PB_fleet-mgr-publisher.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicles-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_vehicles-subscriber.json

export gw_url="mqtt-sample-scenario1.southcentralus-1.mqtt.eventgrid-int.azure.net"
