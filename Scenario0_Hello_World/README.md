# Scenario 0 – Hello World
This is a hello world scenario, with a publisher and subscriber communicating on a single topic.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|Pub_client | Publisher | sample/topic |
|Sub_client	 | Subscriber | sample/topic |

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|pub-client | all0 | pub-hello| hello  -Topic Templates: sample/#  -Subscription Support: LowFanout|
|sub-client| all0 | sub-hello|  hello  -Topic Templates: sample/#  -Subscription Support: LowFanout|

You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**

- Run this command to configure the script `chmod 700 create_resources.sh`

- Edit the script "create_resources.sh" to change the subscription id and resource group:
```bash
sub_id="<your Subscription ID>"
rg_name="<your Resource Group name>"
```
- Run the script to configure all the resources: `./create_resources.sh`

**Configure the resources manually:**
-Set the following variables to use in the following commands:
```bash
ns_name="mqtt-sample-Scenario0"
sub_id="d48566a8-2428-4a6c-8347-9675d09fb851"
rg_name="slb-rg"
base_type="Microsoft.EventGrid/namespaces"
resource_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces/${ns_name}"
```
- Create a namespace:
```bash
az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario0.json
```
- Generate certificates using the cert-gen scripts. You can skip this step if you're using your own certificate.
```bash
pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate pub-client
./certGen.sh create_leaf_certificate_from_intermediate sub-client
popd
```
- Edit the CAC_test-ca-cert.json to input the certificate string:
	- Go to ./MQTTBrokerPrivatePreview/cert-gen/certs/azure-mqtt-test-only.intermediate.cert.pem 
	- Copy string between -----BEGIN CERTIFICATE----- and -----END CERTIFICATE-----
	- Paste the string in ./MQTTBrokerPrivatePreview/Scenario0_Hello_World/resources/CAC_test-ca-cert.json. 
		- To put the cert string as a one line in the json, use ("End" button>"Delete" button) until all the string is in one line in the json

- Create the CA Certificate:
az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json

- Create the following clients:
	- pub-client
	- sub-client
```bash
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/pub-client --api-version 2022-10-15-preview --properties @./resources/C_pub-client.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/sub-client --api-version 2022-10-15-preview --properties @./resources/C_sub-client.json
```
- Create the following client group:
	- all0
		- Query: name IN ['pub-client', 'sub-client']
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/all0 --api-version 2022-10-15-preview --properties @./resources/CG_all0.json
```
- Create the following topic space:
	- hello
		- Topic Template: sample/#
		- Subscription Support: LowFanout
```bash
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/hello --api-version 2022-10-15-preview --properties @./resources/TS_hello.json
```
- Create the following permission bindings:
	- pub-hello: to grant access for the client group CG_all0 to publish to the topic space TS_hello
	- sub-hello: to grant access for the client group CG_all0 to subscribe to the topic space TS_hello
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/sub-hello --api-version 2022-10-15-preview --properties @./resources/PB_sub-hello.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/pub-hello --api-version 2022-10-15-preview --properties @./resources/PB_pub-hello.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/publish.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/subscribe.py`
