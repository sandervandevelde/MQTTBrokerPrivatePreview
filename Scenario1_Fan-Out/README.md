# Scenario 1 – Fan-out (one-to-many) messages
This scenario simulates cloud-to-device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alerts to all the vehicles in the fleet.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|s1-fleet-mgr | Publisher | fleets/alerts/weather/alert1|
|s1-vehicle1 | Subscriber | fleets/alerts/#|
|s1-vehicle2 | Subscriber | fleets/alerts/#|

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|fleet-mgt-client (Attributes: “Type”:”Fleet-Mgmt”)| fleet-mgr| fleet-mgr-publisher|  weather-alerts (Topic template: fleet/alerts/weather/alert1 -Subscription Support: HighFanout)|
|s1-vehicle1 (Attributes: “Type”:”Vehicle”)| vehicles| vehicles-subscriber|  weather-alerts (Topic template: fleet/alerts/# -Subscription Support: NotSupported)|
|s1-vehicle2 (Attributes: “Type”:”Vehicle”)| vehicles| vehicles-subscriber|  weather-alerts (Topic template: fleet/alerts/# -Subscription Support: NotSupported)|

Follow the instructions in the Prerequisites to test this scenarios. You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**
- Run the following commands to run the script, creating the resources: 
```bash
chmod 700 create_resources.sh
./create_resources.sh
```

**Configure the resources manually:**
- Set a unique namespace name in the following varibale to be used in the following commands
```bash
export resource_prefix="${ns_id_prefix}/<unique namespace name>"
```
- Create a namespace:
```bash
az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario1.json
```
- Generate certificates using the cert-gen scripts. You can skip this step if you're using your own certificate.
```bash
pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s1-vehicle1
./certGen.sh create_leaf_certificate_from_intermediate s1-vehicle2
./certGen.sh create_leaf_certificate_from_intermediate s1-fleet-mgr
popd
```
- Create the CA Certificate:
```bash
az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json
```
- Register the following clients:
	- s1-fleet-mgr
		- Attribute: Type=management
	- s1-vehicle1
		- Attribute: Type=vehicle
	- s1-vehicle2
		- Attribute: Type=vehicle
```bash

az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-fleet-mgr --api-version 2022-10-15-preview --properties @./resources/C_fleet-mgr.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s1-vehicle2 --api-version 2022-10-15-preview --properties @./resources/C_vehicle2.json
```
- Create the following client groups:
	- fleet-mgr to include the s1-fleet-mgr client
		- Query: ${client.attribute.Type}= “management”
	- vehicles to include s1-vehicle1 and s1-vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/fleet-mgr --api-version 2022-10-15-preview --properties @./resources/CG_fleet-mgr.json
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicles --api-version 2022-10-15-preview --properties @./resources/CG_vehicles.json
```
- Create the following topic space:
	- weather-alerts
		- Topic Template: fleets/alerts/#
		- Subscription Support: HighFanout
```bash
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/weather-alerts --api-version 2022-10-15-preview --properties @./resources/TS_weather-alerts.json
```
- Create the following permission bindings:
	- PB_fleet-mgr-publisher: to grant access for the client group fleet-mgr to publish to the topic space weather-alerts
	- vehicles-subscriber: to grant access for the client group vehicles to subscribe to the topic space weather-alerts
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/fleet-mgr-publisher --api-version 2022-10-15-preview --properties @./resources/PB_fleet-mgr-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicles-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_vehicles-subscriber.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open two terminal windows in your Linux environment, navigate to the scenario directory in both windows, and then run the following commands in both windows after editing the \<namespace name>:
```bash
# Make sure you have the `mqtt-broker` virtual environment activated 
source ~/env/mqtt-broker/bin/activate
# Set up the following variable
export gw_url="<namespace name>.eastus2euap-1.ts.eventgrid.azure.net"
```
3. In one terminal window, run the subscribe sample script through the following command: `python ./subscribe.py`.
4. In the other terminal window, run the publish sample script through the following command: `python ./publish.py`.
5. Observe the messages in the published messages in the subscribe terminal window.
