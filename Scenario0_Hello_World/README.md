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


**Configure the resources:**

- Create a namespace
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name> --is-full-object --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\NS_Scenario0.json
```
- Register the following clients:
	- pub-client
	- sub-client
```bash
az resource create --resource-type ${base_type}/clients --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name>/clients/pub-client --api-version 2022-10-15-preview --properties @./resources/C_pub-client.json

az resource create --resource-type ${base_type}/clients --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name>/clients/sub-client --api-version 2022-10-15-preview --properties @./resources/C_sub-client.json
```
- Create the following client group:
	- all0
		- Query: name IN ['pub-client', 'sub-client']
```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name>/clientGroups/all0 --api-version 2022-10-15-preview --properties @C:\jsons\Scenario4\CG_all0.json
```
- Create the following topic space:
	- hello
		- Topic Template: sample/#
		- Subscription Support: LowFanout
```bash
az resource create --resource-type ${base_type}/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name>/topicSpaces/hello --api-version 2022-10-15-preview --properties @./resources/TS_hello.json
```
- Create the following permission bindings:
	- pub-hello: to grant access for the client group CG_all0 to publish to the topic space TS_hello
	- sub-hello: to grant access for the client group CG_all0 to subscribe to the topic space TS_hello
```bash
az resource create --resource-type ${base_type}/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name>/permissionBindings/sub-hello --api-version 2022-10-15-preview --properties @./resources/PB_sub-hello.json

az resource create --resource-type ${base_type}/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/<resource group>/providers/Microsoft.EventGrid/namespaces/<namespace name>/permissionBindings/pub-hello --api-version 2022-10-15-preview --properties @./resources/PB_pub-hello.json
```

**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/publish.py`
4. In a different terminal window, set up the following variable: `gw_url="<namespace name>.southcentralus-1.mqtt.eventgrid-int.azure.net"` and run the sample script through the following command: `python python/subscribe.py`
