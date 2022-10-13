### Get started with Azure CLI:

This quickstart requires Azure CLI version 2.17.1 or later. Run the following command to find the cuurent installed version
    
    az --version
    
To install or upgrade, see [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
    

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

    ```bash
# Create the topic in the Central US EUAP Region and set the input schema to CloudEvent Schema v1.0
az eventgrid topic create -g <resource group> --name <topic name> -l centraluseuap --input-schema cloudeventschemav1_0
# Register the Event Grid resource provider
az provider register --namespace Microsoft.EventGrid
# Set EventGrid Data Sender role to your user ID
az role assignment create --assignee "<alias>@contoso.com" --role "EventGrid Data Sender" --scope "/subscriptions/<subscription ID>/resourcegroups/<resource group>/providers/Microsoft.EventGrid/topics/<event grid topic name>"
    ```

### Namespace

#### ARM Contract
~~~
{
  "properties": {
    "topicSpacesConfiguration": {
      "state": "Enabled"
      "routeTopicResourceId": "/subscriptions/<Subscription ID>/resourceGroups/<Resource Group>/providers/Microsoft.EventGrid/topics/<Event Grid Topic name>",
    },
    "location": "centraluseuap",
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
| Create namespace |  az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name> --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS.json | 
Get namespace | az resource show --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name> |
Delete Namespace | az resource delete --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name> |


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
| Create caCertificate |  az resource create --resource-type Microsoft.EventGrid/namespaces/caCertificates --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/caCertificates/\<Ca Certificate Name> --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json | 
Get caCertificate | az resource show --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/caCertificates/\<Ca Certificate Name> |
Delete caCertificate | az resource delete --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/caCertificates/\<Ca Certificate Name> |



### Clients

#### ARM Contract
> Note: Only one authentication property type (from CertificateThumbprint or CertificateSubject) must be provided in the Create/Update Payload for Client.

##### For CA Certificate Subject based authentication
~~~
{
  "properties": {
    "state": "Enabled",
    "authentication": {
      "certificateSubject": {
        "commonName": "client.mqtt.contoso.com",
        "countryCode": "US",
        "organization": "Contoso",
        "organizationUnit": "IoT"
      }
    },
    "attributes": {
        "attribute1": "345",
        "arrayAttribute": [
            "value1",
            "value2",
            "value"
        ]
    },
    "description": "This is a test client"
  },
}
~~~

##### For Self-Signed Certificate Thumbprint based authentication
~~~
{
  "properties": {
    "state": "Enabled",
    "authentication": {
        "certificateThumbprint": {
            "primary": "primaryThumbprint",
            "secondary": "secondaryThumbprint"
        }
      }
    },
    "attributes": {
        "attribute1": "345",
        "arrayAttribute": [
            "value1",
            "value2",
            "value"
        ]
    },
    "description": "This is a test client"
  },
}
~~~

#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create Client | az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/clients/\<Client Name> --api-version 2022-10-15-preview --properties @./resources/client.json | 
Get Client | az resource show --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/clients/\<Client Name> |
Delete Client | az resource delete --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/clients/\<Client Name> |


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
| Create clientGroup |  az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/clientGroups/\<Client Group Name> --api-version 2022-10-15-preview --properties @./resources/CG.json | 
Get clientGroup | az resource show --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/clientGroups/\<Client Group Name> |
Delete clientGroup | az resource delete --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/clientGroups/\<Client Group Name>|


### Topic Spaces

#### ARM Contract
~~~
{ 
    "properties":{
        "subscriptionSupport": "LowFanout",
        "topicTemplates": [
            "segment1/+/segment3/${client.name}",
            "segment1/${client.attributes.attribute1}/segment3/#"
        ]
    }
}
~~~
#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create topicSpace |  az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/topicSpaces/\<Topic Space Name> --api-version 2022-10-15-preview --properties @./resources/TS.json | 
Get topicSpace | az resource show --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/topicSpaces/\<Topic Space Name> |
Delete topicSpace | az resource delete --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/topicSpaces/\<Topic Space Name> |



### Permission Binding

#### ARM Contract
~~~
{
  "properties": {
    "clientGroupName": "clientGroup1",
    "permission": "Publisher", //or Subscriber
    "topicSpaceName": "topicSpace1"
  },
}
~~~
#### Commands
| Action           | Azure CLI |
| ---------------- | --------- |
| Create permissionBinding |  az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/permissionBindings/\<Permission Binding Name> --api-version 2022-10-15-preview --properties @./resources/PB.json | 
Get permissionBinding | az resource show --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/permissionBindings/\<Permission Binding Name> |
Delete permissionBinding | az resource delete --id /subscriptions/\<Subscription ID>/resourceGroups/\<Resource Group>/providers/Microsoft.EventGrid/namespaces/\<Namespace Name>/permissionBindings/\<Permission Binding Name> |




