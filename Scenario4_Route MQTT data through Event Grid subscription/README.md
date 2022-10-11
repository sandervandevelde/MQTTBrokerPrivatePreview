# Scenario 4 – Route MQTT data through Event Grid subscription
This scenario showcases how to configure routing to send filtered messages from the MQTT Broker to an  Event Hub instance. Consider a use case where one needs to identify the location of vehicles, and want to route the vehicles’ location data from each area to a separate event hub instance.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|Vehicle1 | Publisher | areas/area1/vehicles/vehicle1/GPS|

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|Vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles | Vehicles-Pub|  VehiclesLocation: -Topic Templates: areas/+/vehicles/${principal.deviceid}/GPS/#  -Subscription Support: Not supported|


**Configure the resources:**

- Configure your Event Grid Topic where your messages will be routed.
```bash
# Create the topic in the Central US EUAP Region and set the input schema to CloudEvent Schema v1.0
az eventgrid topic create -g <resource group> --name <topic name> -l southcentralus --input-schema cloudeventschemav1_0
# Register the Event Grid resource provider
az provider register --namespace Microsoft.EventGrid
# Set EventGrid Data Sender role to your user ID
az role assignment create --assignee "<alias>@contoso.com" --role "EventGrid Data Sender" --scope "/subscriptions/<subscription ID>/resourcegroups/<resource group>/providers/Microsoft.EventGrid/topics/<event grid topic name>"
```
- Create a namespace with a reference to the Event Grid Topic that you just created
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4 --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\NS_Scenario4.json
```

- Register the following clients:
	- Vehicle1
		- Attribute: Type=vehicle
		- Authentication: self-signed certificate
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\C_Vehicle1.json
```

- Create the following client groups:
	- Vehicles to include vehicle1 client
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\CG_Vehicles.json
```
- Create the following topic space:
	- VehiclesLocation 
		- Topic Template: vehicles/${principal.deviceid}/GPS/#
		- Subscription Support: Not supported
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/topicSpaces/VehiclesLocation --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\TS_VehiclesLocation.json
```
- Create the following permission bindings:
	- Vehicles-Pub: to grant access for the client group Vehicles to publish to the topic space VehiclesLocation
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/permissionBindings/Vehicles-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\PB_Vehicles-Pub.json
```
- In the portal, go to the created Event Grid topic > Event subscription menu item, and select Event subscription.
- Provide the following fields:
	- Name: event subscription name
	- Event Schema: Cloud Event Schema v1.0
	- Endpoint type: Event Hubs
	- Endpoint: your Event Hubs endpoint
- Go to the “Filters” tab, and “Enable subject filtering”
	- In the field “Subject Begins With”, type “areas/area1/vehicles/”
		- The MQTT topic is represented by the Subject field in the routed Cloud Event Schema so this configuration will filter all the messages with the MQTT Topic that starts with “areas/area1/vehicles/”.


**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. Set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"`
4. Run the sample script through `python python/publish_1.py`
