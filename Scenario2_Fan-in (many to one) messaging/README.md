# Scenario 2 – Fan-in (many to one) messaging
This scenario simulates device to cloud communication and can be leveraged for use cases such as sending telemetry to the backend service. Consider a use case where the backend service needs to identify the location of vehicles on a map. Vehicles should be prohibited from listening to other vehicles’ locations or publishing other vehicles’ location on their behalf.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|s2-map-client | Subscriber | vehicles/+/GPS |
|s2-vehicle1 | Publisher | vehicles/vehicle1/GPS |
|s2-vehicle2 | Publisher | vehicles/vehicle2/GPS |

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|s2-map-client (Attributes: “Type”:”Mapping”)| map | map-subscriber |  subscribe: -Topic Templates: vehicles/+/GPS -Subscription Support: LowFanout |
|s2-vehicle1 (Attributes: “Type”:”Vehicle”)| vehicles| vehicles-publisher |  publish: -Topic Templates: vehicles/${client.name}/GPS -Subscription Support: NotSupported |
|s2-vehicle2 (Attributes: “Type”:”Vehicle”)| Vehicles| vehicles-publisher |  publish: -Topic Templates: vehicles/${client.name}/GPS -Subscription Support: NotSupported |

You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**
- Run this command to configure the script `chmod 700 create_resources.sh`

- Edit the script "create_resources.sh" to change the subscription id and resource group:
```bash
sub_id="<your Subscription ID>"
rg_name="<your Resource Group name>"
```
- Run the script to configure all the resources: `./create_resources.sh`

**Configure the resources manually:**
- Set the following variables to use in the following commands:
```bash
ns_name="mqtt-sample-Scenario2"
sub_id="<your Subscription ID>"
rg_name="<your Resource Group name>"
base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces/${ns_name}"
```
- Create a namespace:
```bash
az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario2.json
```
- Generate certificates using the cert-gen scripts. You can skip this step if you're using your own certificate.
```bash
pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s2-vehicle1
./certGen.sh create_leaf_certificate_from_intermediate s2-vehicle2
./certGen.sh create_leaf_certificate_from_intermediate s2-map-client
popd
```
- Edit the CAC_test-ca-cert.json to input the certificate string:
	- Go to ./MQTTBrokerPrivatePreview/cert-gen/certs/azure-mqtt-test-only.intermediate.cert.pem 
	- Copy string between -----BEGIN CERTIFICATE----- and -----END CERTIFICATE-----
	- Paste the string in ./MQTTBrokerPrivatePreview/Scenario0_Hello_World/resources/CAC_test-ca-cert.json. 
		- To put the cert string as a one line in the json, use ("End" button>"Delete" button) until all the string is in one line in the json
- Create the CA Certificate:
```bash
az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json
```
- Register the following clients:
	- s2-map-client
		- Attribute: Type=mapping
	- s2-vehicle1
		- Attribute: Type=vehicle
	- s2-vehicle2
		- Attribute: Type=vehicle
```bash
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s2-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s2-vehicle2 --api-version 2022-10-15-preview --properties @./resources/C_vehicle2.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s2-map-client --api-version 2022-10-15-preview --properties @./resources/C_map-client.json
```
- Create the following client groups:
	- map to include the Map_Client
		- Query: ${client.attribute.Type}= “mapping”
	- vehicles to include vehicle1 and vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/map --api-version 2022-10-15-preview --properties @./resources/CG_map.json
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicles --api-version 2022-10-15-preview --properties @./resources/CG_vehicles.json
```
- Create the following topic spaces:
	- subscribe:
		- Topic Templates: vehicles/+/GPS
		- Subscription Support: LowFanout
	- publish:
		- Topic Templates: vehicles/${client.name}/GPS
		- Subscription Support: NotSupported
```bash
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/publish --api-version 2022-10-15-preview --properties @./resources/TS_publish.json
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/subscribe --api-version 2022-10-15-preview --properties @./resources/TS_subscribe.json
```

- Create the following permission bindings:
	- map-subscriber: to grant access for the client group MapClients to subscribe to the topic space LocationDataRecieved
	- vehicles-publisher: to grant access for the client group Vehicles to publish to the topic space LocationDataPublished
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicles-publisher --api-version 2022-10-15-preview --properties @./resources/PB_vehicles-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/map-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_map-subscriber.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/publish.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/subscribe.py`
