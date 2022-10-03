#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/bdf55cdd-8dab-4cf4-9b2f-c21e8a780472/resourceGroups/slbojanic-rg/providers/Microsoft.EventGrid/namespaces"

az resource create --resource-type ${base_type} --id ${resource_prefix}/Scenario0 --is-full-object --api-version 2022-10-15-preview --properties @./Scenario0_jsons/NS_Scenario0.json

az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/Scenario0/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./Scenario0_jsons/CACertificate.json

az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/Scenario0/topicSpaces/hello --api-version 2022-10-15-preview --properties @./Scenario0_jsons/TS_hello.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/Scenario0/clients/pub_client --api-version 2022-10-15-preview --properties @./Scenario0_jsons/C_pub_client.json

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/Scenario0/clients/sub_client --api-version 2022-10-15-preview --properties @./Scenario0_jsons/C_sub_client.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/Scenario0/permissionBindings/sub_hello --api-version 2022-10-15-preview --properties @./Scenario0_jsons/PB_subscriber.json

az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/Scenario0/permissionBindings/pub_hello --api-version 2022-10-15-preview --properties @./Scenario0_jsons/PB_publisher.json

# armclient (PowerShell)

$BasePath = "/subscriptions/68032991-d62b-4402-98dc-c4fa84054a6c/resourceGroups/test-eg/providers/Microsoft.EventGrid"

armclient PUT $BasePath/namespaces/Scenario0/caCertificates/test-ca-cert?api-version=2022-10-15-preview .\Scenario0_jsons\CACertificate.json

armclient PUT $BasePath/namespaces/Scenario0/topicSpaces/hello?api-version=2022-10-15-preview .\Scenario0_jsons\TS_hello.json

armclient PUT $BasePath/namespaces/Scenario0/clients/pub_client?api-version=2022-10-15-preview .\Scenario0_jsons\C_pub_client.json

armclient PUT $BasePath/namespaces/Scenario0/clients/sub_client?api-version=2022-10-15-preview .\Scenario0_jsons\C_sub_client.json

armclient PUT $BasePath/namespaces/Scenario0/permissionBindings/sub-hello?api-version=2022-10-15-preview .\Scenario0_jsons\PB_subscriber.json

armclient PUT $BasePath/namespaces/Scenario0/permissionBindings/pub-hello?api-version=2022-10-15-preview .\Scenario0_jsons\PB_publisher.json

armclient PUT $BasePath/namespaces/Scenario0/clientGroups/foo?api-version=2022-10-15-preview .\Scenario1_jsons\CG_Vehicles.json




az resource show --resource-type ${base_type}/clientGroups --id ${resource_prefix}/Scenario0/clientGroups/$all --api-version 2022-10-15-preview