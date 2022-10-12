# Scenario 3 – One to one messaging
This scenario simulates the request-response messaging pattern. Request-response uses two topics, one for the request and one for the response.

Consider a use case where a user can unlock their car from a mobile app. The request to unlock are published on vehicles/unlock/req/<carClientId>/<mobileClientId> and the response of unlock operation are published on vehicles/unlock/res/<mobileClientId>/<carClientId>.

**Scenario:**

| Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
| s3-mobile1 | Publisher | vehicles/unlock/req/car1/mobile1|
| s3-mobile1 | Subscriber | vehicles/unlock/res/mobile1/#|
| s3-vehicle1 | Publisher | vehicles/unlock/res/mobile1/car1|
| s3-vehicle1 | Subscriber | vehicles/unlock/req/car1/#|

**Resource Configuration:**
| Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|s3-mobile1 (Attributes: "Type"="mobile")| Mobiles| MobileClients-Pub|  UnlockPublish -Topic Template: -vehicles/unlock/req/+/${client.name} -vehicles/unlock/res/+/${client.name} -Subscription Support: Not supported |
|s3-mobile1 (Attributes: "Type"="mobile")| Mobiles| MobileClients-Sub|  UnlockSubscribe -Topic Template: -vehicles/unlock/req/\${client.name}/# -vehicles/unlock/res/\${client.name}/# -Subscription Support: LowFanout|
|s3-vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles| Vehicles-Pub |  UnlockPublish -Topic Template: -vehicles/unlock/req/+/\${client.name} -vehicles/unlock/res/+/${client.name} -Subscription Support: Not supported |
|s3-vehicle1 (Attributes: “Type”:”vehicle”)| Vehicles| Vehicles-Sub |  UnlockSubscribe -Topic Template: -vehicles/unlock/req/\${client.name}/# -vehicles/unlock/res/${client.name}/# -Subscription Support: LowFanout |

You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**
- Run this command to configure the script `chmod 700 create_resources.sh`

- Edit the script "create_resources.sh" to change the subscription id and resource group variables to include the values of your own Subscription ID and Resource Group name:
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
./certGen.sh create_leaf_certificate_from_intermediate s3-vehicle1
./certGen.sh create_leaf_certificate_from_intermediate s3-mobile1
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
	- s3-mobile1
		- Attribute: Type=mobile
	- s3-vehicle1
		- Attribute: Type=vehicle
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clients/Mobile1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\C_Mobile1.json

az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario3/clients/Vehicle1 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario3\C_Vehicle1.json
```
- Create the following client groups:
	- MobileClients to include the s3-mobile1 client
		- Query: ${client.attribute.Type}= “mobile”
	- Vehicles to include s3-vehicle1 client
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
