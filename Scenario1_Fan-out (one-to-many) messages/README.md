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

**Configure the resources:**
- Create a namespace
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1 --is-full-object --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\NS_Scenario1.json
```
- Register the following clients:
	- Fleet_mgmt_device
		- Attribute: Type=management
	- Vehicle1
		- Attribute: Type=vehicle
	- Vehicle2
		- Attribute: Type=vehicle

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/clients/fleet_mgt_client --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\C_fleet_mgt_client.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/clients/vehicle1 --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\C_vehicle1.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/clients/vehicle2 --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\C_vehicle2.json
```
- Create the following client groups:
	- Fleet-mgmt to include the Fleet_mgmt_device client
		- Query: ${client.attribute.Type}= “management”
	- Vehicles to include vehicle1 and vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/clientGroups/FleetMgmt --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\CG_FleetMgmt.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\CG_Vehicles.json
```
- Create the following topic space:
	- WeatherAlerts
		- Topic Template: fleets/alerts/#
		- Subscription Support: HighFanout
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/topicSpaces/WeatherAlerts --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\TS_WeatherAlerts.json
```
- Create the following permission bindings:
	- FleetMgmt-Pub: to grant access for the client group Flee-mgmt to publish to the topic space WeatherAlerts
	- Vehicles-Sub: to grant access for the client group Vehicles to subscribe to the topic space WeatherAlerts
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/permissionBindings/FleetMgmt-publisher --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\PB_FleetMgmt-publisher.json

az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1/permissionBindings/Vehicles-subscriber --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\PB_Vehicles-subscriber.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/publish.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/subscribe.py`
