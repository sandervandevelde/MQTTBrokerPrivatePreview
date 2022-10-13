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
|s3-mobile1 (Attributes: "Type"="mobile")| mobile| mobile-publisher|  mobile-publish (Topic Template: vehicles/unlock/req/+/${client.name} -Subscription Support: Not supported) |
|s3-mobile1 (Attributes: "Type"="mobile")| mobile| mobile-subscriber|  mobile-subscribe (Topic Template: vehicles/unlock/res/${client.name}/# -Subscription Support: LowFanout)|
|s3-vehicle1 (Attributes: “Type”:”vehicle”)| vehicle| vehicle-publisher |  vehicle-publish (Topic Template: vehicles/unlock/res/+/${client.name} -Subscription Support: Not supported) |
|s3-vehicle1 (Attributes: “Type”:”vehicle”)| vehicle| vehicle-subscriber |  vehicle-subscribe (Topic Template: vehicles/unlock/req/${client.name}/# -Subscription Support: LowFanout) |

Follow the instructions in the [Prerequisites](#prerequisites) to test this scenarios. You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**
- Run the following commands to run the script, creating the resources: 
```bash
chmod 700 create_resources.sh
./create_resources.sh
```

**Configure the resources manually:**
- Create a namespace:
```bash
az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario3.json
```
- Generate certificates using the cert-gen scripts. You can skip this step if you're using your own certificate.
```bash
pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s3-vehicle1
./certGen.sh create_leaf_certificate_from_intermediate s3-mobile1
popd
```
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
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s3-mobile1 --api-version 2022-10-15-preview --properties @./resources/C_mobile1.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s3-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json
```
- Create the following client groups:
	- mobile to include the s3-mobile1 client
		- Query: ${client.attribute.Type}= “mobile”
	- vehicle to include s3-vehicle1 client
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/mobile --api-version 2022-10-15-preview --properties @./resources/CG_mobile.json
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicle --api-version 2022-10-15-preview --properties @./resources/CG_vehicle.json
```		
- Create the following topic spaces:
	- mobile-publish:
		- Topic Templates:
			- vehicles/unlock/req/+/${client.name}
		- Subscription Support: NotSupported
	- mobile-subscribe:
		- Topic Templates:
			- vehicles/unlock/res/${client.name}/#
		- Subscription Support: LowFanout
	- vehicle-publish:
		- Topic Templates:
			- vehicles/unlock/res/+/${client.name}
		- Subscription Support: NotSupported
	- vehicle-subscribe:
		- Topic Templates:
			- vehicles/unlock/req/${client.name}/#
		- Subscription Support: LowFanout
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicle-publisher --api-version 2022-10-15-preview --properties @./resources/PB_vehicle-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicle-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_vehicle-subscriber.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/mobile-publisher --api-version 2022-10-15-preview --properties @./resources/PB_mobile-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/mobile-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_mobile-subscriber.json
```
- Create the following permission bindings:
	- mobile-publisher: to grant access for the client group mobile to publish to the topic space mobile-publish
	- mobile-subscriber: to grant access for the client group mobile to subscribe to the topic space mobile-subscribe
	- vehicle-publisher: to grant access for the client group vehicle to publish to the topic space vehicle-publish
	- vehicle-subscriber: to grant access for the client group vehicle to subscribe to the topic space vehicle-subscribe
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/mobile-publisher --api-version 2022-10-15-preview --properties @./resources/PB_mobile-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/mobile-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_mobile-subscriber.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicle-publisher --api-version 2022-10-15-preview --properties @./resources/PB_vehicle-publisher.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicle-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_vehicle-subscriber.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `export gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python ./vehicle_device.py`
4. In a different terminal window, set up the following variable: `export gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python ./mobile_device.py`
