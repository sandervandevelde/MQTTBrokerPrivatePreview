# Scenario 2 – Fan-in (many to one) messaging
This scenario simulates device to cloud communication and can be leveraged for use cases such as sending telemetry to the backend service. Consider a use case where the backend service needs to identify the location of vehicles on a map. Vehicles should be prohibited from listening to other vehicles’ locations or publishing other vehicles’ location on their behalf.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|Map_Client | Subscriber | vehicles/+/GPS |
|Vehicle1 | Publisher | vehicles/vehicle1/GPS |
|Vehicle2 | Publisher | vehicles/vehicle2/GPS |

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|Map_Client (Attributes: “Type”:”Mapping”)| MapClients | MapClients-Sub |  LocationDataRecieved: -Topic Templates: vehicles/+/GPS -Subscription Support: LowFanout |
|vehicle1 (Attributes: “Type”:”Vehicle”)| Vehicles| Vehicles-Pub |  LocationDataPublished: -Topic Templates: vehicles/${client.name}/GPS -Subscription Support: NotSupported |
|vehicle2 (Attributes: “Type”:”Vehicle”)| Vehicles| Vehicles-Pub |  LocationDataPublished: -Topic Templates: vehicles/${client.name}/GPS -Subscription Support: NotSupported |

**Configure the resources:**
- Create a namespace
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2 --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\NS_Scenario2.json
```
- Register the following clients:
	- Map_Client 
		- Attribute: Type=mapping
	- Vehicle1
		- Attribute: Type=vehicle
	- Vehicle2
		- Attribute: Type=vehicle
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clients/Map_Client --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\C_Map_Client.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\C_Vehicle1.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clients/Vehicle2 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\C_Vehicle2.json
```
- Create the following client groups:
	- MapClients to include the Map_Client
		- Query: ${client.attribute.Type}= “mapping”
	- Vehicles to include vehicle1 and vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clientGroups/MapClients --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\CG_MapClients.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\CG_Vehicles.json
```
- Create the following topic spaces:
	- LocationDataRecieved:
		- Topic Templates: vehicles/+/GPS
		- Subscription Support: LowFanout
	- LocationDataPublished:
		- Topic Templates: vehicles/${client.name}/GPS
		- Subscription Support: NotSupported
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/topicSpaces/LocationDataRecieved --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\TS_LocationDataRecieved.json

az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/topicSpaces/LocationDataPublished --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\TS_LocationDataPublished.json
```

- Create the following permission bindings:
	- MapClients-Sub: to grant access for the client group MapClients to subscribe to the topic space LocationDataRecieved
	- Vehicles-Pub: to grant access for the client group Vehicles to publish to the topic space LocationDataPublished
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/permissionBindings/MapClients-Sub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\PB_MapClients-Sub.json

az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/permissionBindings/Vehicles-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\PB_Vehicles-Pub.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/publish.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/subscribe.py`
