# Scenario 1 – Fan-out (one-to-many) messages
This scenario simulates cloud-to-device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alerts to all the vehicles in the fleet.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|Fleet-mgmt-device | Publisher | fleets/alerts/weather/alert1|
|Vehicle1 | Subscriber | fleets/alerts/#|
|Vehicle2 | Subscriber | fleets/alerts/#|

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|fleet-mgt-client (Attributes: “Type”:”Fleet-Mgmt”)| FleetMgmt| FleetMgmt-publisher|  WeatherAlerts (Topic template: fleet/alerts/weather/alert1) -Subscription Support: HighFanout|
|vehicle1 (Attributes: “Type”:”Vehicle”)| Vehicles| Vehicles-subscriber|  WeatherAlerts (Topic template: fleet/alerts/#) -Subscription Support: NotSupported|
|vehicle2 (Attributes: “Type”:”Vehicle”)| Vehicles| Vehicles-subscriber|  WeatherAlerts (Topic template: fleet/alerts/#) -Subscription Support: NotSupported|


![Deploy to Azure](https://aka.ms/deploytoazurebutton)

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
ns_name="mqtt-sample-Scenario1"
sub_id="<your Subscription ID>"
rg_name="<your Resource Group name>"
base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces/${ns_name}"
```
- Create a namespace:
```bash
az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario1.json
```
- Generate certificates using the cert-gen scripts. You can skip this step if you're using your own certificate.
```bash
pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate pub-client
./certGen.sh create_leaf_certificate_from_intermediate sub-client
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
	- Fleet_mgmt_device
		- Attribute: Type=management
	- Vehicle1
		- Attribute: Type=vehicle
	- Vehicle2
		- Attribute: Type=vehicle

```bash

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-fleet-mgr --api-version 2022-10-15-preview --properties @./resources/C_fleet-mgr.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-vehicle2 --api-version 2022-10-15-preview --properties @./resources/C_vehicle2.json
```
- Create the following client groups:
	- Fleet-mgmt to include the Fleet_mgmt_device client
		- Query: ${client.attribute.Type}= “management”
	- Vehicles to include vehicle1 and vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/fleet-mgr --api-version 2022-10-15-preview --properties @./resources/CG_fleet-mgr.json
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicles --api-version 2022-10-15-preview --properties @./resources/CG_vehicles.json
```
- Create the following topic space:
	- WeatherAlerts
		- Topic Template: fleets/alerts/#
		- Subscription Support: HighFanout
```bash
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/weather-alerts --api-version 2022-10-15-preview --properties @./resources/TS_weather-alerts.json
```
- Create the following permission bindings:
	- FleetMgmt-Pub: to grant access for the client group Flee-mgmt to publish to the topic space WeatherAlerts
	- Vehicles-Sub: to grant access for the client group Vehicles to subscribe to the topic space WeatherAlerts
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/fleet-mgr-publisher --api-version 2022-10-15-preview --properties @./resources/PB_fleet-mgr-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicles-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_vehicles-subscriber.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/publish.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/subscribe.py`
