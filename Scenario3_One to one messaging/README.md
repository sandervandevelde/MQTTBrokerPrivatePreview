# Scenario 3 – One to one messaging
This scenario simulates the request-response messaging pattern. Request-response uses two topics, one for the request and one for the response.

Consider a use case where a user can unlock their car from a mobile app. The request to unlock are published on vehicles/unlock/req/<carClientId>/<mobileClientId> and the response of unlock operation are published on vehicles/unlock/res/<mobileClientId>/<carClientId>.

**Scenario:**

| Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
| Mobile1 | Publisher | vehicles/unlock/req/car1/mobile1|
| Mobile1 | Subscriber | vehicles/unlock/res/mobile1/#|
| Vehicle1 | Publisher | vehicles/unlock/res/mobile1/car1|
| Vehicle1 | Subscriber | vehicles/unlock/req/car1/#|

**Resource Configuration:**
| Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
| Mobile1 (Attributes: "Type"="mobile")| Mobiles| MobileClients-Pub|  UnlockPublish -Topic Template: -vehicles/unlock/req/+/${client.name} -vehicles/unlock/res/+/${client.name} -Subscription Support: Not supported |
|Mobile1 (Attributes: "Type"="mobile")| Mobiles| MobileClients-Sub|  UnlockSubscribe -Topic Template: -vehicles/unlock/req/\${client.name}/# -vehicles/unlock/res/\${client.name}/# -Subscription Support: LowFanout|
|Vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles| Vehicles-Pub |  UnlockPublish -Topic Template: -vehicles/unlock/req/+/\${client.name} -vehicles/unlock/res/+/${client.name} -Subscription Support: Not supported |
|Vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles| Vehicles-Sub |  UnlockSubscribe -Topic Template: -vehicles/unlock/req/\${client.name}/# -vehicles/unlock/res/${client.name}/# -Subscription Support: LowFanout |


**Configure the resources:**
- Create a namespace
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3 --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\NS_Scenario3.json
```
- Register the following clients:
	- Mobile1
		- Attribute: Type=mobile
	- Vehicle1
		- Attribute: Type=vehicle
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clients/Mobile1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\C_Mobile1.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\C_Vehicle1.json
```
- Create the following client groups:
	- MobileClients to include the Mobile1 client
		- Query: ${client.attribute.Type}= “mobile”
	- Vehicles to include Vehicle1 client
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clientGroups/Mobiles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\CG_Mobiles.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\CG_Vehicles.json
```		
- Create the following topic spaces:
	- UnlockPublish:
		- Topic Templates:
			- vehicles/unlock/req/+/${principal.deviceid}
			- vehicles/unlock/res/+/${principal.deviceid}
		- Subscription Support: NotSupported
	- UnlockSubscribe:
		- Topic Templates:
			- vehicles/unlock/req/${principal.deviceid}/#
			- vehicles/unlock/res/${principal.deviceid}/#
		- Subscription Support: LowFanout
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/topicSpaces/UnlockPublish --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\TS_UnlockPublish.json

az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/topicSpaces/UnlockSubscribe --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\TS_UnlockSubscribe.json
```
- Create the following permission bindings:
	- MobileClients-Pub: to grant access for the client group MobileClients to publish to the topic space UnlockPublish
	- MobileClients-Pub: to grant access for the client group MobileClients to subscribe to the topic space UnlockSubscribe
	- Vehicles-Pub: to grant access for the client group Vehicles to publish to the topic space UnlockPublish
	- Vehicles-Pub: to grant access for the client group Vehicles to subscribe to the topic space UnlockSubscribe


```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/MobileClients-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_MobileClients-Pub.json

az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/MobileClients-Sub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_MobileClients-Sub.json

az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/Vehicles-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_Vehicles-Pub.json

az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/Vehicles-Sub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_Vehicles-Sub.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/mobile_device.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/vehicle_device.py`
