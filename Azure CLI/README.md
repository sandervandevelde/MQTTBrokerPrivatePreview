### Get started with Azure CLI:

This quickstart requires Azure CLI version 2.17.1 or later. Run the following command to find the cuurent installed version
    
    az --version
    
To install or upgrade, see [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
    
- Register Azure Cloud

    ```bash
    az cloud register --name AzureCloud --endpoint-active-directory-resource-id https://management.core.windows.net/ --endpoint-resource-manager https://api-dogfood.resources.windows-int.net/ --endpoint-active-directory  https://login.windows-ppe.net/ --endpoint-active-directory-graph-resource-id https://graph.ppe.windows.net/
    ```
- Set Azure cloud
    ```bash
    az cloud set --name AzureCloud
    ```
- Login to Azure
    ```bash
    az login
    ```

- Set your subscription
    ```bash
    az account set -s <Subscription ID>
    ```
### Event Grid Topic
To route your messages from your clients to different Azure services or your custom endpoint, an Event Grid topic needs to be created and referenced during namespace creation to forward the messages to that topic for routing; this reference cannot be added/updated afterwards. Use the following commands to create the topic and set the right permissions to take advantage of the routing functionality.


    az eventgrid topic create -g ${rg_name} --name ${eg_topic_name} -l southcentralus --input-schema cloudeventschemav1_0
    az provider register --namespace Microsoft.EventGrid
    az role assignment create --assignee "<alias>@microsoft.com" --role "EventGrid Data Sender" --scope "/subscriptions/${sub_id}/resourcegroups/${rg_name}/providers/Microsoft.EventGrid/topics/${eg_topic_name}"


### Namespace

#### ARM Contract
~~~
{
  "properties": {
    "inputSchema": "CloudEventSchemaV1_0",
    "topicSpacesConfiguration": {
      "state": "enabled",
      "routeTopic": "/subscriptions/<Subscription ID>/resourceGroups/<Resource Group>/providers/Microsoft.EventGrid/topics/<Event Grid Topic name>"
    }
  },
  "location": "southcentralus",
  "tags": {
    "tag1": "value1",
    "tag2": "value2",
    "tag3": "value3"
  }
}
~~~


#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create namespace |  az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name> --api-version 2022-10-15-preview --properties @D:\Work\Pub-sub\mqttns.json       | 
Get namespace | az resource show --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name> |
Delete Namespace | az resource delete --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name> |


### CA Certificate

#### ARM Contract
~~~
{
    "properties": {
        "description": "This is a test certificate",
        "encodedCertificate": "-----BEGIN CERTIFICATE-----
{{ Base64 encoded Certificate}}
-----END CERTIFICATE-----"
    }
}
~~~
#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create caCertificate |  az resource create --resource-type Microsoft.EventGrid/namespaces/caCertificates --id /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/caCertificates/\<caCertificateName>--api-version 2022-10-15-preview --properties @D:\Work\Pub-sub\caCertificate.json | 
Get caCertificate | az resource show --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/caCertificates/\<caCertificate-name> |
Delete caCertificate | az resource delete --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/caCertificates/\<name> |



### Clients

#### ARM Contract
> [!Note]
>One and only one authentication type properties (from CertificateThumbprint or CertificateSubject) must be provided in the Create/Update Payload for Client.

##### For CA Certificate Subject based authentication
~~~
{
    "properties": {
        "isEnabled": true,
        "authentication": {
            "certificateSubject": {
                "commonName": "CertificateCommonName",
                "organization": "Microsoft",
                "organizationUnit": "Azure",
                "countryCode": "US"
            }
        },
        "attributes": {
            "room": "345",
            "floor": 3,
            "deviceTypes": [
                "Fan",
                "Light",
                "AC"
            ]
        },
        "description": "This is a test client"
    }
}
~~~

##### For Self-Signed Certificate Thumbprint based authentication
~~~
{
    "properties": {
        "isEnabled": true,
        "authentication": {
            "certificateThumbprint": {
                "primary": "primaryThumbprint",
                "secondary": "secondaryThumbprint"
            }
        },
        "attributes": {
            "room": "345",
            "floor": 3,
            "deviceTypes": [
                "Fan",
                "Light",
                "AC"
            ]
        },
        "description": "This is a test client"
    }
}
~~~

#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create Client | az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/clients/\<ClientName>--api-version 2022-10-15-preview --properties @D:\Work\Pub-sub\client.json | 
Get Client | az resource show --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/clients/\<Client-name> |
Delete Client | az resource delete --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/clients/\<name>|


### Client Groups

#### ARM Contract
~~~
{
    "properties": {
        "description": "This is a test client group",
        "query": "attributes.b IN ['a', 'b', 'c']"
    }
}
~~~

#### Commands
| Action           |Azure CLI |
| ---------------- | --------- |
| Create clientGroup |  az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/clientGroups/\<clientGroupName>--api-version 2022-10-15-preview --properties @D:\Work\Pub-sub\clientGroup.json | 
Get clientGroup | az resource show --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/clientGroups/\<clientGroup-name> |
Delete clientGroup | az resource delete --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/clientGroups/\<name>|


### Topic Spaces

#### ARM Contract
~~~
{ 
    "properties":
    {
        "topicTemplates":["filter3","filter4"],
        "subscriptionSupport":"LowFanout"
    }

}
~~~
#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create topicSpace |  az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/topicSpaces/\<topicSpaceName>--api-version 2022-10-15-preview --properties @D:\Work\Pub-sub\topicSpace.json | 
Get topicSpace | az resource show --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/topicSpaces/\<topicSpace-name> |
Delete topicSpace | az resource delete --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/topicSpaces/\<name> |



### Permission Binding

#### ARM Contract
~~~
{
    "properties":{
        "principalId":"<ARM ID of Device Group>",
        "scope":"<ARM ID of Topic SPACE>",
        "roleDefinitionId":"testroleDefinitiofullarmidTest"
    }
}
~~~
#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create permissionBinding |  az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/permissionBindings/\<permissionBindingName>--api-version 2022-10-15-preview --properties @D:\Work\Pub-sub\permissionBinding.json | 
Get permissionBinding | az resource show --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/permissionBindings/\<permissionBinding-name> |
Delete permissionBinding | az resource delete --ids /subscriptions/\<Subscription ID>/resourceGroups/\<resource group name>/providers/Microsoft.EventGrid/namespaces/\<namespace-name>/permissionBindings/\<name> |




