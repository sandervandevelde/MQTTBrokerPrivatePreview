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


**High-level steps:**
- Create a CA Certificate: CaCert1
- Register the following clients:
	- Map_Client 
		- Attribute: Type=mapping
	- Vehicle1
		- Attribute: Type=vehicle
	- Vehicle2
		- Attribute: Type=vehicle
- Create the following client groups:
	- MapClients to include the Map_Client
		- Query: ${client.attribute.Type}= “mapping”
	- Vehicles to include vehicle1 and vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
- Create the following topic spaces:
	- LocationDataRecieved:
		- Topic Templates: vehicles/+/GPS
		- Subscription Support: LowFanout
	- LocationDataPublished:
		- Topic Templates: vehicles/${client.name}/GPS
		- Subscription Support: NotSupported
- Create the following permission bindings:
	- MapClients-Sub: to grant access for the client group MapClients to subscribe to the topic space LocationDataRecieved
	- Vehicles-Pub: to grant access for the client group Vehicles to publish to the topic space LocationDataPublished




**CLI Instructions:**

Download the folder Scenario1_jsons with JSON files to C:

Replace the \<Subscription ID\> with your subscription ID in below commands.

Create the namespace under the resource group that you already created as part of the prerequisites.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2 --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\NS_Scenario2.json
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
az resource create --resource-type Microsoft.EventGrid/namespaces/caCertificates --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/caCertificates/CACert --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\MqttCACertificate.json
```

Onboard the Clients using below CLI commands.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clients/Map_Client --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\C_Map_Client.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\C_Vehicle1.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clients/Vehicle2 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\C_Vehicle2.json
```

Create the Client Groups using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clientGroups/MapClients --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\CG_MapClients.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\CG_Vehicles.json
```

Create the Topic Spaces using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/topicSpaces/LocationDataRecieved --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\TS_LocationDataRecieved.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/topicSpaces/LocationDataPublished --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\TS_LocationDataPublished.json
```

Create the Permission Bindings using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/permissionBindings/MapClients-Sub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\PB_MapClients-Sub.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario2/permissionBindings/Vehicles-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario2\PB_Vehicles-Pub.json
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

