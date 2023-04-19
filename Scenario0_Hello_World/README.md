# Scenario 0 – Hello World
This is a hello world scenario, with a publisher and subscriber communicating on a single topic.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|pub_client | Publisher | samples/topic |
|sub_client	 | Subscriber | samples/topic |

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|pub-client | all0 | pub-hello| hello  (Topic Templates: samples/#  -Subscription Support: LowFanout)|
|sub-client| all0 | sub-hello|  hello  (Topic Templates: samples/#  -Subscription Support: LowFanout)|

Follow the instructions in the Prerequisites to test this scenarios. You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**
- Run the following commands to run the script, creating the resources: 
```bash
chmod 700 create_resources.sh
./create_resources.sh
```

**Configure the resources manually:**
- Set a unique namespace name in the following varibale to be used in the following commands
```bash
export resource_prefix="${ns_id_prefix}/<unique namespace name>"
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
- Create the CA Certificate:
```bash
az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json
```
- Create the following clients:
	- pub-client
	- sub-client
```bash
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/pub-client --api-version 2022-10-15-preview --properties @./resources/C_pub-client.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/sub-client --api-version 2022-10-15-preview --properties @./resources/C_sub-client.json
```
- Create the following client group:
	- all0 to include pub-client and sub-client clients
		- Query: name IN ['pub-client', 'sub-client']
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/all0 --api-version 2022-10-15-preview --properties @./resources/CG_all0.json
```
- Create the following topic space:
	- hello
		- Topic Template: samples/#
		- Subscription Support: LowFanout
```bash
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/hello --api-version 2022-10-15-preview --properties @./resources/TS_hello.json
```
- Create the following permission bindings:
	- pub-hello: to grant access for the client group all0 to publish to the topic space hello
	- sub-hello: to grant access for the client group all0 to subscribe to the topic space hello
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/sub-hello --api-version 2022-10-15-preview --properties @./resources/PB_sub-hello.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/pub-hello --api-version 2022-10-15-preview --properties @./resources/PB_pub-hello.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open two terminal windows in your Linux environment, navigate to the scenario directory in both windows, and then run the following commands in both windows after editing the \<namespace name>:
```bash
# Make sure you have the `mqtt-broker` virtual environment activated 
source ~/env/mqtt-broker/bin/activate
# Set up the following variable
export gw_url="<namespace name>.eastus2euap-1.ts.eventgrid.azure.net"
```
3. In one terminal window, run the subscribe sample script through the following command: `python ./subscribe.py`.
4. In the other terminal window, run the publish sample script through the following command: `python ./publish.py`.
5. Observe the messages in the published messages in the subscribe terminal window.

