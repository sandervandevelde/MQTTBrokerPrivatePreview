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
| Mobile1 (Attributes: "Type"="mobile")| Mobiles| MobileClients-Pub|  UnlockPublish -Topic Template: -vehicles/unlock/req/+/${principal.deviceid} -vehicles/unlock/res/+/${principal.deviceid} -Subscription Support: Not supported |
|Mobile1 (Attributes: "Type"="mobile")| Mobiles| MobileClients-Sub|  UnlockSubscribe -Topic Template: -vehicles/unlock/req/\${principal.deviceid}/# -vehicles/unlock/res/\${principal.deviceid}/# -Subscription Support: LowFanout|
|Vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles| Vehicles-Pub |  UnlockPublish -Topic Template: -vehicles/unlock/req/+/\${principal.deviceid} -vehicles/unlock/res/+/${principal.deviceid} -Subscription Support: Not supported |
|Vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles| Vehicles-Sub |  UnlockSubscribe -Topic Template: -vehicles/unlock/req/\${principal.deviceid}/# -vehicles/unlock/res/${principal.deviceid}/# -Subscription Support: LowFanout |


**High-level steps:**
- Register the following clients:
	- Mobile1
		- Attribute: Type=mobile
	- Vehicle1
		- Attribute: Type=vehicle
- Create the following client groups:
	- MobileClients to include the Mobile1 client
		- Query: ${client.attribute.Type}= “mobile”
	- Vehicles to include Vehicle1 client
		- Query: ${client.attribute.Type}= “vehicle”
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
- Create the following permission bindings:
	- MobileClients-Pub: to grant access for the client group MobileClients to publish to the topic space UnlockPublish
	- MobileClients-Pub: to grant access for the client group MobileClients to subscribe to the topic space UnlockSubscribe
	- Vehicles-Pub: to grant access for the client group Vehicles to publish to the topic space UnlockPublish
	- Vehicles-Pub: to grant access for the client group Vehicles to subscribe to the topic space UnlockSubscribe


**CLI Instructions:**

Download the folder Scenario1_jsons with JSON files to C:

Replace the \<Subscription ID\> with your subscription ID in below commands.

Create the namespace under the resource group that you already created as part of the prerequisites.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3 --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\NS_Scenario3.json
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
az resource create --resource-type Microsoft.EventGrid/namespaces/caCertificates --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/caCertificates/CACert --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\MqttCACertificate.json
```

Onboard the Clients using below CLI commands.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clients/Mobile1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\C_Mobile1.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\C_Vehicle1.json
```

Create the Client Groups using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clientGroups/Mobiles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\CG_Mobiles.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\CG_Vehicles.json
```

Create the Topic Spaces using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/topicSpaces/UnlockPublish --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\TS_UnlockPublish.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/topicSpaces/UnlockSubscribe --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\TS_UnlockSubscribe.json
```

Create the Permission Bindings using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/MobileClients-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_MobileClients-Pub.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/MobileClients-Sub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_MobileClients-Sub.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/Vehicles-Pub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_Vehicles-Pub.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/permissionBindings/Vehicles-Sub --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\PB_Vehicles-Sub.json
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

