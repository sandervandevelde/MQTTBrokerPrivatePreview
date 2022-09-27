# Scenario 4 – Route MQTT data through Event Grid subscription
This scenario showcases how to configure routing to send filtered messages from the MQTT Broker to an  Event Hub instance. Consider a use case where one needs to identify the location of vehicles, and want to route the vehicles’ location data from each area to a separate event hub instance.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|Vehicle1 | Publisher | areas/area1/vehicles/vehicle1/GPS|

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|Vehicle1 (Attributes: “Type”:”Fleet_Mgmt”)| Vehicles | Vehicles-Pub|  VehiclesLocation: -Topic Templates: areas/+/vehicles/${principal.deviceid}/GPS/#  -Subscription Support: Not supported|


**High-level steps:**
- Make sure you used the routing ARM template during the namespace creation to create the Event Grid topic where the MQTT data will be routed.
- Register the following clients:
	- Vehicle1
		- Attribute: Type=vehicle
		- Authentication: self-signed certificate > PrimaryThumbprint
- Create the following client groups:
	- Vehicles to include vehicle1 client
		- Query: ${client.attribute.Type}= “vehicle”
- Create the following topic space:
	- VehiclesLocation 
		- Topic Template: vehicles/${principal.deviceid}/GPS/#
		- Subscription Support: Not supported
- Create the following permission bindings:
	- Vehicles-Pub: to grant access for the client group Vehicles to publish to the topic space VehiclesLocation
- In the portal, go to the created Event Grid topic > Event subscription menu item, and select Event subscription.
- Provide the following fields:
	- Name: event subscription name
	- Event Schema: Cloud Event Schema v1.0
	- Endpoint type: Event Hubs
	- Endpoint: your Event Hubs endpoint
- Go to the “Filters” tab, and “Enable subject filtering”
	- In the field “Subject Begins With”, type “areas/area1/vehicles/”
		- The MQTT topic is represented by the Subject field in the routed Cloud Event Schema so this configuration will filter all the messages with the MQTT Topic that starts with “areas/area1/vehicles/”.



**CLI Instructions:**

Download the folder Scenario1_jsons with JSON files to C:

Replace the \<Subscription ID\> with your subscription ID in below commands.

Create the namespace under the resource group that you already created as part of the prerequisites.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4 --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\NS_Scenario4.json
```

If you are using a CA certificate to authenticate the clients, the encoded certificate string must be in valid PEM (Privacy Enhanced Mail) format with header (-----BEGIN CERTIFICATE-----) and footer (-----END CERTIFICATE-----). This string must not include a private key. Save the certificate as a json file named MqttCACertificate.json in C:\Scenario1_jsons\ folder.  You can include a description in the properties as below.

```json
{
    "properties":{
   	    "description": "This is a CA certificate",
        "encodedCertificate": "-----BEGIN CERTIFICATE-----
			---Base64 encoded Certificate---
 -----END CERTIFICATE-----"
    }
}
```

Register the CA Certificate using the below command.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/caCertificates --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/caCertificates/CACert --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\MqttCACertificate.json
```

Onboard the Clients using below CLI commands.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\C_Vehicle1.json
```


Create the Client Groups using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\CG_Vehicles.json
```


Create the Topic Spaces using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/topicSpaces/VehiclesLocation --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\TS_VehiclesLocation.json
```

Create the Permission Bindings using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario4/permissionBindings/Vehicles-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\PB_Vehicles-Pub.json
```



**Instructions to deploy using ARM template on portal:**

1. Go to Azure portal, type "deploy a custom template" in the search.

<img src="Deploy ARM template on portal 1.png"
     alt="Deploy ARM template on portal 1"
     style="float: left; margin-right: 10px;" />


2. Select "Deploy a custom template" from the Services list.  Click on "Build your own template in the editor".

<img src="Deploy ARM template on portal 2.png"
     alt="Deploy ARM template on portal 2"
     style="float: left; margin-right: 10px;" />

3. Copy the json from the "ARM template for all resources.json" file in the scenario's json folder into the editor.  Click the save button.
	 
<img src="Deploy ARM template on portal 3.png"
     alt="Deploy ARM template on portal 3"
     style="float: left; margin-right: 10px;" />

4. Check the subscription and select the resource group.  Click on the "Reveiw + Create" button to initiate the deployment.

<img src="Deploy ARM template on portal 4.png"
     alt="Deploy ARM template on portal 4"
     style="float: left; margin-right: 10px;" />

5. You will see the screen that deployment is in progress, wait till it's successful.  Once it shows the deployment is successful, you can see the list of all the resources created for the scenario.

<img src="Deploy ARM template on portal 5.png"
     alt="Deploy ARM template on portal 5"
     style="float: left; margin-right: 10px;" />

