# MQTT broker functionality in Event Grid

The Microsoft Azure Messaging team invites you and your organization to preview the MQTT broker functionality in Event Grid.  During this preview, we will provide full support with a high level of engagement from the Azure Messaging product group.  Please note that this preview is available by invitation only and requires an NDA.  By participating in the private preview, you agree to the [Terms of Use](https://www.microsoft.com/legal/terms-of-use).  Please submit the [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURURXNEw4UkpTOEdNVTVXSllLQVhBUUo0US4u) to signup for private preview.  We look forward to your feedback as you leverage this capability. You can submit your feedback using this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURDA2RVRTV1VBSUQ2MDBCM1g3WkY4Q1k2Sy4u).  

## Overview
MQTT broker functionality in Event Grid delivers the flexibility to leverage hierarchical topics and supports messaging using the light weight MQTT protocol.  Clients (both devices and cloud applications) can publish and subscribe over these flexible topics for scenarios such as command and control and high scale broadcast.



|Concepts|
| ------------ |
| [MQTT standard protocol](https://mqtt.org/) |
| [Client Authentication](#client-authentication) |
| [Client Groups](#client-groups) |
| [Topic Spaces](#topic-spaces)|

## Private preview program information
The private preview is only for testing.  Please do NOT use it for your production.

**Engagement:**  We will actively engage with you during the preview. At any point, feel free to connect with us for questions/concerns by emailing to askmqtt@microsoft.com.

**Feedback:**  At the end of the preview, we will capture additional feedback using this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURDA2RVRTV1VBSUQ2MDBCM1g3WkY4Q1k2Sy4u).

**Cost to use:**  For this release, MQTT broker functionality in Event Grid is available for no additional charge. You will be charged for routing MQTT messages through Event Grid subscriptions.  Please check the Event Grid pricing [here](https://azure.microsoft.com/en-us/pricing/details/event-grid/).

**Supported Region**
This private preview is currently supported only in Central US EUAP region.

**Post private preview program**
When the private preview program ends, or when your tests are completed, you can choose to either cleanup your configuration or retain the configuration in private preview Central US EUAP region region.


## Capabilities available in this preview
This private preview provides the following capabilities
- Cloud MQTT broker functionality in Event Grid enabling publish and subscribe on flexible topic structure: support of wildcards in topic structure to allow subscription to filtered messages
- MQTT v3.1.1. compliance with limitations (LWT, Retain messages, Message ordering and QoS 2 are not supported) 
- QoS 0, 1: MQTT manages the re-transmission of messages and guarantees delivery making communication in unreliable networks a lot reliable.
- Flexible access control model:  Grouping clients into "client groups" and topic references into topic spaces to ease access control management.
- Fine-grained access control model:  Introducing "topic templates" with variables support to enable fine-grained access control.
- Support for 1-1, 1-many and many-1 messaging patterns to accommodate for a variety of scenarios
- Compatibility with standard MQTT client libraries (ex. Eclipse Paho) allows users to migrate configuration much faster
- Route MQTT messages through Event Grid subscriptions to integrate data with Azure services or custom endpoints for flexibility to further process the data
- Persistent session will allow for clean session if client disconnects and reconnects, ensuring subscribed messages are sent after reconnection.
- Support for TLS 1.2 endpoints for data plane operations to keep the data transmission secure
- Also, see [throttle limit tables](#limits) below

## Capabilities coming up in future releases
The following features are not in scope for this release, but they will be supported in future -
- Azure Portal UX, CLI, custom Azure SDK libraries along with APIs
- MQTT v5 support
- Ability to publish messages to topics using HTTP
- Edge MQTT Broker bridging
- Last Will and Testament (LWT) support
- Retain flag support
- Metrics and diagnostic logs 
- Large message of 512KB 
- TLS 1.3 support
- Enhanced performance and scale limits 
- Pay As You Go Billing


## Prerequisites

- We will enable the feature for the subscription ID you shared in the sign up form. If you haven't responded, please fill out this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURURXNEw4UkpTOEdNVTVXSllLQVhBUUo0US4u)

- You can use any ARM client to deploy the service's resources and any compliant MQTT client to test the service. However, this guide will only provide commands and scripts using [Azure CLI](/Azure%20CLI/README.md) for deploying resouces and Paho client in python for testing in Ubuntu. Follow these steps to take advantage of the provided instructions: 
	1. Use any Linux environment for testing.
		- To easily install and run Linux on Windows, run `wsl --install -d Ubuntu`. After installation is complete, you can run `wsl` to start running commands on your Ubuntu subsystem whenever you open a new terminal window. [Learn more](https://learn.microsoft.com/en-us/windows/wsl/)
	2. Clone this repository to any directory in your Linux environment: `git clone https://github.com/Azure/MQTTBrokerPrivatePreview.git`
	3. Follow the instructions in the [Environment_configuration README](/Environment_configuration/README.md) to register Azure CLI and set common variables for resources deployment.
	4. Follow the instructions in the [Python README](https://github.com/Azure/MQTTBrokerPrivatePreview/tree/main/python#azure-mqtt-broker-sample-python-instructions) to be able to test the scenarios.
	5. Navigate to each of the scenario folders and follow its README.md instructions to run the scenario.

- To connect to the new MQTT broker functionality in Event Grid, the clients must be authenticated using X.509 certificates. Clients can be authenticated using a CA-signed certificate or a self-signed certificate.  Please see the [client authentication section](#client-authentication). You can use your own certificates or the certificate generation script provided in this guide and referenced in the scenarios' instructions.

- To route your messages from your clients to different Azure services or your custom endpoint, an Event Grid topic needs to be created and referenced during namespace creation to forward the messages to that topic for routing; this reference cannot be added/updated afterwards. [Scenario4](/Scenario4_Route%20MQTT%20data%20through%20Event%20Grid%20subscription) showcases an example of of the configuration to take advantage of the routing functionality and the [Routing and Namespace sections of the generic Azure CLI instructions](https://github.com/Azure/MQTTBrokerPrivatePreview/tree/main/Azure%20CLI#event-grid-topic) also provide instructions on the generic routing configuration.  


## QuickStart
Let us get started with a simple scenario, with a publisher and subscriber communicating on a topic. 

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|Pub_client | Publisher | samples/topic |
|Sub_client | Subscriber | samples/topic |

After following the instructions in the [Prerequisites](#prerequisites), navigate to the Scenario0_Hello_World folder in your cloned repo through `cd ./MQTTBrokerPrivatePreview/Scenario0_Hello_World/`

Run the following commands to run the script, creating the resources: 
```bash
chmod 700 create_resources.sh
./create_resources.sh
```
To test the scenario:
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `mqtt-broker` virtual environment activated by running `source ~/env/mqtt-broker/bin/activate` in Linux or `env/mqtt-broker/bin/activate` in Windows
3. In a terminal window, set up the following variable: `export gw_url="<namespace name>.southcentralus-1.ts.eventgrid.azure.net"` and run the sample script through the following command: `python ./subscribe.py`
4. In a different terminal window, set up the following variable: `export gw_url="<namespace name>.southcentralus-1.ts.eventgrid.azure.net"` and run the sample script through the following command: `python ./publish.py`


## Scenarios
Here are a few scenarios that showcase the functionality of the service. Follow the instructions in the [Prerequisites](#Prerequisites) to test these scenarios.

| # | Scenario | Description |
| ------------ | ------------ | ------------ |
| 1 | Fan-out (one-to-many) messages  | This scenario simulates cloud-to-client commands to several clients and can be leveraged for use cases such as sending alerts to clients. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet. For instructions see [README](/Scenario1_Fan-out%20(one-to-many)%20messages/README).  |
| 2 | Fan-in (many to one) messaging  | This scenario simulates publishing messages from multiple clients to a single client.  Consider a use case where one needs to identify location of vehicles on a map.  For instructions see [README](/Scenario2_Fan-in%20(many%20to%20one)%20messaging/README). |
| 3 | One to one messaging  | This scenario simulates publishing messages from one client to another.  Consider a use case where a user can unlock their car from a mobile app.  For instructions see [README](/Scenario3_One%20to%20one%20messaging/README.md).  |
| 4 | Route MQTT data through Event Grid subscription  | This scenario showcases how to configure route to send filtered messages from MQTT to the endpoint: Event Hubs through EG subscription.  Consider a use case where one needs to identify location of vehicles.  For instructions see [README](/Scenario4_Route%20MQTT%20data%20through%20Event%20Grid%20subscription/README.md).  |


Please share your feedback using this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURDA2RVRTV1VBSUQ2MDBCM1g3WkY4Q1k2Sy4u) or email us at askmqtt@microsoft.com with any questions you may have.


## Terminology
Some of the key terms relevant for private preview are explained below.

| Term| Definition |
| ------------ | ------------ |
| MQTT Broker| An MQTT broker is an intermediary entity that enables MQTT clients to communicate. Specifically, an MQTT broker receives messages published by clients, filters the messages by topic, and distributes them to subscribers. |
| Namespace| A namespace is a declarative region that provides a scope to the resources (certificates, clients, client groups, topic spaces, permission bindings, etc.) inside it.  Namespaces are used to organize the resources into logical groups. |
| Client| Client can be a device or a service that will publish and/or subscribe MQTT messages |
| Certificate / Cert| Certificate is a form of asymmetric credential. They are a combination of a public key from an asymmetric keypair and a set of metadata describing the valid uses of the keypair.  If the keypair of the issuer is the same keypair as the certificate, the certificate is said to be "self-signed". Third-party certificate issuers are sometimes called Certificate Authorities (CA). |
| Client attributes| Client attributes represent a set of key-value pairs that provide descriptive information about the client.  Client attributes are used in creating client groups and as variables in Topic Templates.   For example, client type is an attribute that provides the client's type. |
| Client group| Client group is a collection of clients that are grouped by a set of common client attribute(s) using a query string, and could be allowed to publish and/or subscribe to a specific Topic Spaces |
| Topic spaces | Topic spaces is a set of topic templates (defined below). It is used to simplify access control management by enabling you to grant publish or subscribe access to a group of topics at once instead of individual topics. |
| Topic filter| An MQTT topic filter is an MQTT topic that can include wildcards for one or more of its segments, allowing it to match multiple MQTT topics. It is used to simplify subscriptions declarations as one topic filter can match multiple topics. |
| Topic template| Topic templates are an extension of the topic filter that supports variables. It is used for fine-grained access control within a client group. |
| Permission bindings| A Permission Binding grants access to a specific client group to either publish or subscribe on a specific topic spaces.  |

## Concepts

### Client Authentication
For private preview, we will be supporting authentication of clients using X.509 certificates.  X.509 certificate will provide the credentials to associate a particular client with the tenant, and at the same time, ensure the communication is encrypted.  In this model, authentication generally happens once during session establishment.  Then, all future operations using the same session are assumed to come from that identity. 
The following credential types are supported:
- Certificates issued by a Certificate Authority (CA) 
- Self-signed certificates

**CA signed certificates:**  In this method, a root or intermediate X.509 certificate is registered with the service.  Essentially, the root or intermediary certificate that is used to sign the client certificate, must be registered with the service first.  Later, clients are authenticated if they have a valid leaf certificate that's signed by the root or intermediate certificate that was supplied to the service.  While registering the clients, the subject common name of the leaf certificate needs to be supplied for authentication. Service will validate the subject values match the subject values from the client certificate and also validate the client certificate is signed the root or intermediary certificate that was registered earlier.  

**Self-signed certificates:**  For self-signed certificates, clients are onboarded to the service using the certificate thumbprint alongside the identity record. In this method of authentication, the client registry will store the exact ID of the certificate that the client is going to use to authenticate. 

One and only one authentication type properties (CertificateThumbprint or CertificateSubject) must be provided in the Create/Update Payload for Client.

### Client Groups
Client group is a new concept introduced to make management of client access controls (publish/subscribe) easy – multiple clients can be grouped together based on certain commonalities to provide similar levels of authorization to publish and/or subscribe to Topic spaces.

Clients can be devices or applications, such as devices or vehicles that send/receive MQTT messages. We provide a default client group, named $all, which all clients are associated with. For ease of testing, you can considering using $all for premissions.

For example, a fleet management company with hundreds of trucks and other shipment delivery vehicles across the country, can improve their routing, tracking, driver safety and predictable maintenance capabilities by sending and receiving MQTT messages to/from the vehicles to/from monitoring applications on cloud.

In this scenario, vehicles can be configured as clients that publish/subscribe to various topics such as weather information, road conditions, geo location, engine performance and other wear-and-tear aspects of the vehicle.  And, while configuring the vehicle as a client, a set of attributes such as vehicle type, year, make & model, max load capacity can also be included as part of the client metadata via client attributes.

These client attributes can be used to create the client groups.  For example, if the vehicles that can carry loads over 2 tons are prone to accidents if driven with low braking fluid, in icy road conditions, then all such vehicles can be grouped together to continuously monitor and alert the drivers in case of potential hazardous conditions based on weather at their locations.

### Client group considerations:
The main purpose of client groups is to provide common authorization to a set of clients to either publish and/or subscribe on one or more Topic spaces.  Every client needs to be part of a client group to be able to publish and subscribe on topic spaces.  The goal is to keep the quantity of client groups very small to make permissions manageable.
For this preview, we will be supporting a maximum of 10 client groups per namespace.

Clients need to be grouped in a way that it’s easier to reuse the group to publish and subscribe across multiple topic spaces.  To this end, it is important to think through the end-to-end scenarios to identify the topics every client will publish from/subscribe to.  We recommend identifying the commonalities across the scenarios, to avoid over fragmentation of client groups and topic spaces.  Set the client attributes generic enough to achieve simple grouping and avoid highly complex group queries.

**What are client attributes?**
Client attributes are a set of user defined key-value pairs or tags that provide information about the client.  These attributes will be the main ingredient in the client group filtering expressions.  Attributes could be describing the physical or functional characteristics of the client.  Typical attribute could be type of the client (client type).  
Here is an example:
- Type: Values could be "sensor" or "thermostat" or "vehicle"

Here’s a sample schema for the attribute definition: 

```json
{  
    "id": "device123",  
    "attributes": {  
        "status": "active",
        "sensors": ["motion", "noise", "light"]  
     }  
}
```

While configuring the client attributes, consider the topics that the clients will be publishing (subscribing) to.  Thinking backwards from topics to clients will help identifying the commonalities across client roles much easier and defining the client attributes to make the client grouping effortless.  

**How to create client group queries?**
To setup a client group, user needs to build a query that filters a set of clients based on their attribute values.

Here are a few sample queries:
- (attributes.sensors = "motion" or attributes.sensors = "humidity") or attributes.status <> "sleep mode"
- attributes.sensors IN ["motion", "humidity", "temperature"] and attributes.floor <= 5

In group queries, following operands are allowed:
- Equality operator "="
- Not equal operator in 2 forms "<>" and "!=" 
- Less than "<", greater than ">", less than equal to "<=", greater than equal to ">=" for long integer values
- "IN" to compare with a set of values

Please refer to the [naming considerations table](#naming-considerations) for details on allowed characters and patterns.


### Topic Spaces
Topic space is a new concept introduced to simplify management of topics used for publishing and subscribing by your clients.

**Topic space:**  A topic space is a set of topic templates (defined below). It is used to simplify access control management by enabling you to grant publish or subscribe access to a group of topics at once instead of individual topics.  
It is important to note that the publishing is a supported action on all topic spaces by default; however, you need to configure the subscription support as detailed below.

**Topic filter:**  An [MQTT topic filter](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718106) is an MQTT topic that can include wildcards for one or more of its segments, allowing it to match multiple MQTT topics. It is used to simplify subscriptions declarations as one topic filter can match multiple topics.

The service supports all the MQTT wildcards defined by the [MQTT specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718107) as follows:
- +: which matches a single segment.
	- E.g. topic filter: "machines/+/alert" will match the following topics:
		- machines/temp/alert
		- vehicles/humidity/alert
- #: which matches zero or more segments at the end of the topic. 
	- E.g. topic filter: "machines/#" will match the following topics:
		- machines
		- machines/temp
		- machines/humidity
		- machines/temp/alert etc

See [Topic Wilcards](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718107) from the MQTT spec for more details.

**Topic template:** Topic templates are an extension of the topic filter that supports variables. It is used for fine-grained access control within a client group. You can provide access to a client group to publish or subscribe on a topic space with multiple topic templates. If any of the topic templates include a variable, only the clients associated with this variable will have access to the corresponding topic.

For example, you can provide access to client group "machines" to the topic space "machinesTelemetry" that includes the topic template "machines/${client.name}/temp". Only the machine with client name = machine1 will be able to publish on topic "machines/machine1/temp", and only the machine with client name = machine2 will be able to publish on topic "machines/machine2/temp", and so on. This prevents machine2 from publishing false information on behalf of machine1, even though it has access to the same topic space, and vice versa. 

**Supported variables:**
- ${client_name}: this variable represents the name of the client assigned during client creation.
- ${client.attributes.x}: this variable represents any of the assigned attributes to a client during client creation/update, so as "x" would be equal to the exact string of the attribute key. Read more about client attributes in the Terminology section.

**Note:** A variable can represent a portion of a segment or an entire segment but cannot cover more than one segment. E.g. a topic template could include "machines/${client.name|.factory1}/temp" will match topics "machines/machine1.factory1/temp", "machines/machine2.factory1/temp", etc

**Subscription support:** Subscription support is used to optimize the service’s mode of  message delivery to your clients based on your scenario. There are three modes: 
- Not supported: will indicate that topic space could be used only for publishing. This will be helpful in scenarios when you expect your corresponding topic templates to overlap since this is the only mode that will allow your topic templates to overlap with any other topic template.
- Low fanout: will specify a subscription delivery mode optimized for having a maximum of 10 subscribers per topic, with very low latency. 
	- Example scenario: There is a group of vehicles with each vehicle subscribing to its own command delivered to its own topic.
- High fanout: will specify a subscription delivery mode optimized for having unlimited number of subscribers per topic, with higher latency.
	- Example scenario: There is a large group of vehicles in a city subscribing to the same weather alerts that get broadcasted on the same topic.

#### Topic space considerations
- **Default Behavior:**
To publish or subscribe to any topic, a matching topic space must be configured, and a permission binding needs to be set for the client group(s) that include the clients that need publish/subscribe access to this topic space. 
- **Topic templates Overlap:**
If you set your topic space with a low fanout or high fanout subscription modes, the corresponding topic templates cannot overlap with each other, but they can overlap with a topic space with "not supported" subscription support. The overlap exists if a topic could match more than one topic template: 
	- Examples:
		- "machines/${client.name}/temp" and "machines/+/temp" overlap because the second template covers the first one via wildcard. 
		- vehicles/vehicle1/telemetry/# and vehicles/${principal.deviceId}/telemetry/# conflict because in the second template the segment with variable is treated as single level wildcard + and hence, covers the first topic template. PublishOnly topic spaces can overlap with LowFanout topic spaces.
- **Configuration:**
	- Topic templates use special characters $ and | and these need to be escaped differently based on the shell being used. In PowerShell, $ can be escaped with vehicles/${dollar}telemetry/#. If you’re using PowerShell, you can accomplish this as shown in the examples below: 
		- '"vehicles/${principal.deviceId|dollar}/#"'
		- 'vehicles/${principal.deviceId"|"dollar}/#'
	- Subscription support is immutable. To reconfigure the subscription support, delete the topic space and create a new topic space with the desired subscription support.
	- Topic space updates may take up to 5 minutes to propagate.


### Access Control

Client Groups and Topic Spaces are designed to simplify access control. Consider the following as you design Client Groups and Topic Spaces: 
- Group a set of clients into 'Client Groups' such that each Client Group represents the clients that need the same access to publish and/or subscribe to the same set of topics.
- Group a set of Topic Templates into 'Topic Spaces' such that each Topic Space represents messages meant for the same audience (a specific Client Group).

For example:
- Example 1:

    A factory has multiple plants with each plant including Clients that need to communicate with each other. However, Clients from other plants of the factory are not allowed to communicate with them.

	| Client  | Role  | Topic/Topic Filter  |
	| ------------ | ------------ | ------------ |
	|Plant1_Client1| Publisher| plants/plant1/clients/client1|
	|Plant1_Client2| Subscriber| plants/plant1/clients/#|
	|Plant2_Client1| Publisher| plants/plant2/clients/client1|
	|Plant2_Client2| Subscriber| plants/plant2/clients/#|

- Configuration
	- Create a Client Group for each factory plant’s clients.
	- Create a Topic Space for each plant representing the topics that the plant’s clients will communicate over.
	- Create 2 Permission Bindings for each plant’s Client Group to publish and subscribe to its corresponding plant’s Topic Space.


	|Client| Client Group| Permission Binding| Topic Space|
	| ------------ | ------------ | ------------ | ------------ |
	|Plant1_Client1| Plant1Clients| Plant1-Pub| Plant1Messages -Topic Template: plants/plant1/clients/#|
	|Plant1_Client2|Plant1Clients | Plant1-Sub| Plant1Messages -Topic Template: plants/plant1/clients/#|
	|Plant2_Client1| Plant2Clients| Plant2-Pub| Plant2Messages -Topic Template: plants/plant2/clients/#|
	|Plant2_Client2|Plant2Clients | Plant2-Sub| Plant2Messages -Topic Template: plants/plant2/clients/#|

- Example 2:

    Let’s assume an extra requirement for the example above: each plant has management clients and operator clients, and the operator clients must not have publish access in case any of them gets compromised. On the other hand, the management clients need publish access to send commands and subscribe access to receive telemetry.

	| Client | Role | Topic/Topic Filter | 
	| ------------ | ------------ | ------------ |
	| Plant1_OperatorClient1 | Publisher | plants/plant1/OpClients/client1
	|| Subscriber | plants/plant1/MgmtClients/# | 
	| Plant1_MgmtClient1 | Publisher | plants/plant1/MgmtClients/client1
	|| Subscriber | plants/plant1/OpClients/# | 
	| Plant2_OperatorClient1 | Publisher | plants/plant2/OpClients/client1
	| |Subscriber | plants/plant2/MgmtClients/# | 
	| Plant2_ MgmtClient1 | Publisher | plants/plant2/MgmtClients/client1 | 
	||Subscriber | plants/plant2/OpClients/# |

- Configuration:
	- Create 2 Client Groups per plant: one for the management clients and another for the operator clients.
	- Create 2 Topic Spaces for each plant: one representing telemetry topics and another representing commands topics.
	- Create 2 Permission Bindings for each plant’s management clients to publish to the commands Topic Space and subscribe to the telemetry Topic Space.
	- Create 2 Permission Bindings for each plant’s operator clients to subscribe to the commands Topic Space and publish to the telemetry Topic Space.


	|Client | Client Group | Permission Binding | Topic/Topic Filter|
	| ------------ | ------------ | ------------ | ------------ |
	|Plant1_OperatorClient1 | Plant1Operators | Plant1Op-Pub | Plant1Telemetry -Topic Template: plants/plant1/OpClients/#|
	| |  | Plant1Op-Sub | Plant1Commands -Topic Template: plants/plant1/MgmtClients/#|
	|Plant1_MgmtClient1 | Plant1Mgmt | Plant1Mgmt-Pub | Plant1Commands -Topic Template: plants/plant1/MgmtClients/#|
	| |  | Plant1Mgmt-Sub | Plant1Telemetry -Topic Template: plants/plant1/OpClients/#|
	|Plant2_OperatorClient1 | Plant2Operators | Plant2Op-Pub | Plant2Telemetry -Topic Template: plants/plant2/OpClients/#|
	| |  | Plant2Op-Sub | Plant2Commands -Topic Template: plants/plant2/MgmtClients/#|
	|Plant2_ MgmtClient1 | Plant2Mgmt | Plant2Mgmt-Pub | Plant2Commands -Topic Template: plants/plant2/MgmtClients/#|
	| |  | Plant2Mgmt-Sub | Plant2Telemetry -Topic Template: plants/plant2/OpClients/#|
 
### Routing
This functionality will enable you to route your messages from your clients to different Azure services like Event hubs, Service Bus, etc or your custom endpoint. This functionality is achieved through [Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/), by sending all your messages from your clients to an [Event Grid topic](https://docs.microsoft.com/en-us/azure/event-grid/custom-topics), and using [Event Grid subscriptions](https://docs.microsoft.com/en-us/azure/event-grid/subscribe-through-portal) to route the messages from that Event Grid topic to the [supported endpoints](https://docs.microsoft.com/en-us/azure/event-grid/event-handlers).

Event Grid is a highly scalable, serverless event broker that you can use to integrate applications using events. Events are delivered by Event Grid to subscriber destinations such as applications, Azure services, or any endpoint to which Event Grid has network access. [Learn more](https://docs.microsoft.com/en-us/azure/event-grid/)

**Note:**  To be able to take advantage of this feature, you have to either use the ARM template to create the Event Grid custom topic first and provide that topic’s ARM Id during the namespace creation.

[Scenario4](/Scenario4_Route%20MQTT%20data%20through%20Event%20Grid%20subscription/) showcases an example of taking advantage of the routing functionality and the [Routing and Namespace section of the generic Azure CLI instructions](https://github.com/Azure/MQTTBrokerPrivatePreview/tree/main/Azure%20CLI#event-grid-topic) also provides instructions on the routing configuration.  

#### Routing Considerations:
- The Event grid topic that will be used for routing need to fulfil the following requirements:
- It needs to be set to use the Cloud Event Schema v1.0
- It needs to be in the same region as the namespace
- **Filtering:**
	- You can use the Event Grid Subscription’s filtering capability to filter the routed messages based on the MQTT topic through filtering on the "subject" property in the Cloud Event schema. Event Grid Subscriptions supports free simple subject filtering by specifying a starting or ending value for the subject. For example, 
		- You can specify the subject ends with "gps" to only route messages reporting on location. 
		- You can filter the subject begins with "factory1/Area2/" to route only the messages that belong to facotry1 and area 2 to a specific endpoint and you can replicate this configuration to route messages from other factories/areas to different endpoints.
	- You can also take advantage of the [Event Subscription’s advanced filtering](https://docs.microsoft.com/en-us/azure/event-grid/event-filtering#advanced-filtering) to filter based on the MQTT topic through filtering on the subject property in the Cloud Event Schema. This enable you to set more complex filters by secifying a comparison operator, key, and value.

#### The schema for the Cloud Event Schema:
Each message being routed is enveloped in a Cloud Event according to the following schema sample: 
```json
{
    "specversion": "1.0",
    "id": "9aeb0fdf-c01e-0131-0922-9eb54906e20", //Unique id generated by the gateway upon receiving the message
    "time" : "2019-11-18T15:13:39.4589254Z", //Time of message arriving to Azure pub-sub assigned by gateway
    "type" : "MQTT.EventPublished",
    "source"  : "namespace1", //Name of your namespace that received the MQTT message.
    "subject" : "vehicles/ floor1/ vehicleId1/temp" , //MQTT topic that accompanied the MQTT publish message.
    "data_64" : "<Published MQTT message>"
}
```

## Limits
For this release, the following limits are supported.  Please do not stress test beyond the limits mentioned below and for other scenarios.  These limits will be revised for future releases.

|Limit Description | MQTT broker functionality in Event Grid Private Preview |
| ------------ | ------------ |
|Max Message size | 256KB |
|Topic Size| 256KB | 
|New Connect requests | 500/second per namespace |
|Subscribe requests | 5000 messages/second |
|Total number of subscriptions per connection | 50 |
|Total inbound publish requests | 5000 messages/second |
|Total outbound publish requests | 5000 messages/second |
|Total inbound Publish requests per connection | 100/second |
|Total outbound Publish requests per connection | 100/second |

### Resources level limits
| Resource Type | Description| Limit| 
| ------------ | ------------ | ------------ |
| Name spaces | Maximum number of name spaces per subscription | 10 |
| Clients | Maximum number of clients | 10K |
| CA Certificates | Maximum number of registered CA root certificates | 2 |
| Client Groups | Maximum number of client groups| 10 |
| Topic spaces | Maximum number of topic spaces | 10 |
| Topic templates | Maximum number of topic templates within a topic space | 10 |
| Permission bindings | Maximum number of permission bindings | 100 |

## Naming considerations
All the names are of String type

| Category| Name length| Allowed characters| Other considerations|
| ------------ | ------------ | ------------ | ------------ |
| Namespace| 3-50 characters| Alphanumeric, and hyphens(-); no spaces|  Name needs to be unique per region | 
|CA Certificate| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| Name needs to be unique per namespace | 
| Client| 1-128 characters| Alphanumeric, hyphen(-), colon(:), dot(.), and underscore(_), no spaces| Case sensitive; Name needs to be unique per namespace | 
| Client attributes| Total size of the attributes is <=4KB| Alphanumeric and underscores(_)| Case sensitive; Attribute values can be strings, string arrays, integers; Name needs to be unique per namespace| 
| Client Group| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| $all is the default client group that includes all the clients.  This group cannot be edited or deleted; Name needs to be unique per namespace| 
| TopicSpace| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| |
| Permission Bindings| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| Name needs to be unique per namespace | 

## Frequently asked questions 
- Is Azure monitoring metrics and logging available? 
	- Not in this release.  We will add monitoring metrics and diagnostic logs in the next release.
- What happens if client attempts to publish on a topic when a matching topic space is not found? 
	- Client connection will be closed. Identify which client groups the client belongs to.  Based on the permission bindings, identify the topic spaces to which the client groups have access to publish.
- How do I connect to the MQTT broker functionality in Event Grid with a third party tool that requires username and password as string? 
	- Username and password based authentication is not supported in this release.  It will be supported in a future release.
- What happens if I have more than 10 subscribers per topic for a low fanout topic space?
    - In this release, the 11th subscription request for the same topic will be rejected.
- How do Azure IoT Hub and Azure Event Grid compare?
    - While Azure IoT Hub and Azure Event Grid (with new MQTT Broker capability) enable messaging between devices and services, that are necessary for IoT solutions, there are some key differences. Both services support device-to-cloud and cloud-to-device communication but Event Grid also enables device-to-device communication, via the cloud MQTT Broker. IoT Hub provides richer device management and bulk-device provisioning through integration with Azure Device Provisioning Service. In terms of protocols Event Grid supports HTTP & MQTT and IoT Hub supports HTTP, MQTT & AMQP. For messaging use cases using MQTT protocol, you can start with Azure Event Grid. If your solution requires bulk device provisioning and device management, then you can start with Azure IoT Hub. In future, Azure Event Grid will integrate with Azure Device Provisioning Service to enable these bulk provisioning capabilities.




Please share your feedback using this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURDA2RVRTV1VBSUQ2MDBCM1g3WkY4Q1k2Sy4u) or email us at askmqtt@microsoft.com with any questions.

