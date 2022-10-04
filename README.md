# MQTT Broker Private Preview

The Microsoft Azure messaging team invites you and your organization to preview the MQTT functionality.  During this preview, we will provide full support with a high level of engagement from the Azure messaging product group.  Please note that this preview is available by invitation only and requires an NDA.  By participating in the private preview, you agree to the [Terms of Use](https://www.microsoft.com/legal/terms-of-use).  Please submit the [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURURXNEw4UkpTOEdNVTVXSllLQVhBUUo0US4u) to signup for private preview.  We look forward to your feedback as you leverage this capability for your pub/sub solutions. You can submit your feedback using this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURDA2RVRTV1VBSUQ2MDBCM1g3WkY4Q1k2Sy4u).  

## Overview
MQTT Broker delivers a pub/sub messaging broker, to enable secure transfer of messages to and from clients. You can now use MQTT’s flexible topic structure to send and receive messages from your clients (devices/services) and support flexible messaging patterns such as command and control and as well as broadcast messages to clients.

|Concepts|
| ------------ |
| [MQTT standard protocol](https://mqtt.org/) |
| [Client Authentication](#client-authentication) |
| [Client Groups](#client-groups) |
| [Topic Space](#topic-spaces)|

## Private preview program information
The private preview is only for testing.  Please do NOT use it for your production.

**Engagement:**  We will actively engage with you during the preview. At any point, feel free to connect with us for questions/concerns by emailing to mqttbroker@microsoft.com.

**Feedback:**  At the end of the preview, we will capture additional feedback using this form.

**Cost to use:**  For this release, MQTT Broker is available for no additional charge. You will be charged for routing MQTT messages through Event Grid subscriptions (https://azure.microsoft.com/en-us/pricing/details/event-grid/).

## Post private preview program
When the private preview program ends, or when your tests are completed, you can choose to either cleanup your configuration or we can help you migrate the configuration to the public preview space, once it is available. 


## Capabilities available in this preview
This private preview provides the following capabilities
- Cloud MQTT Broker enabling pub/sub on flexible topic structure: support of wildcards in topic structure to allow subscription to filtered messages
- MQTT v3.1.1. compliance with limitations (LWT, Retain messages, Message ordering and QoS 2 are not supported) 
- QoS 0, 1: MQTT manages the re-transmission of messages and guarantees delivery making communication in unreliable networks a lot reliable.
- Flexible access control model:  Grouping clients into “client groups” and topic references into topic spaces to ease access control management.
- Fine-grained access control model:  Introducing “topic templates” with variables support to enable fine-grained access control.
- Support for 1-1, 1-many and many-1 messaging patterns to accommodate for a variety of pub/sub scenarios
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
- Large message of 512KB supported 
- TLS 1.3 support
- Enhanced performance and scale limits 
- Pay As You Go Billing




## Prerequisites

- We will enable the feature for the subscription ID you shared in the sign up form. If you haven't responded, please fill out this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURURXNEw4UkpTOEdNVTVXSllLQVhBUUo0US4u)



**Executing scenarios:**

 To execute the scenarios, you can use either portal or CLI to create resources such as namespace, clients, topicspaces, etc. using the provided ARM templates / JSONs. (You can use other methods such as GitHub deploy to Azure or ARM client to perform these steps)
	- MQTT capability is currently supported only in Central US EUAP region
- To connect to the new MQTT feature, the clients must use authenticated based on X.509 certificates. Clients can be authenticated using a CA signed certificate or a thumbprint of a self-signed certificate. 
    - CA certificate is also a nested resource under the namespace, so each scenario will provide instructions on how to load a CA certificate vs. how to use self-signed certificate.  Once the client is connected regular pub/sub operations will work. 
    - One and only one authentication type properties (from CertificateThumbprint or CertificateSubject) must be provided in the Create/Update Payload for Client.
- To test the message pub/sub, you can use any of your favorite tool.  However, we provided sample code in Python using the Paho MQTT client. You can clone the repo and use it for testing.
    - Current samples for private preview will use existing MQTT libraries and include helper functions that can be used in your own applications.
  
- To route your messages from your clients to different Azure services or your custom endpoint, an Event Grid topic needs to be created and referenced during namespace creation to forward the messages to that topic for routing; this reference cannot be added/updated afterwards. That can be achieved by one of two ways:
	- Use the Namespace-Creation-with-Routing ARM template to create the namespace and the Event Grid topic where the messages will be forwarded.
	- Create an Event Grid topic in the same region as the same namespace and configured to use “Cloud Event Schema v1.0”, then input the topic’s ARM ID as the “routeTopic” during namespace creation.


### Warning
- MQTT capability is in early development and this tech preview is available in the spirit of transparency. Bugs are expected, and we look forward to feedback via email to mqttbroker@microsoft.com.
- Before deviating from the steps in this QuickStart, be sure to review the limitations listed below for the corresponding feature to avoid any confusion.


## QuickStart
Let us get started with a \"hello world\" scenario, with a publisher and subscriber communicating on a topic. Below table enumerates all the resources used in this example.

|Client name|Client Group|PermissionBinding|TopicSpace|
| ------------ | ------------ | ------------ | ------------ |
|Pub_client|Pub_Client_Group|Publisher|sample/topic (Topic template: sample/#)|
|Sub_client|Sub_Client_Group|Subscriber|sample/topic (Topic template: sample/#)|

- Ensure you have the MQTT Broker enabled for the subscription you provided. (--- how? ---)
- For quick start, out of the box, client gets instantiated and runs.  Perform the control plane setup – subscription, namespace details, etc.
- Download all the files in this folder (--- to be added ---).
    - This folder contains all the necessary artifacts required to run the quick start including a sample CA certificate and a .exe file that you can run (--- how/where? ---) to create all the necessary resources.
    - Also, code is made available to customize as per your testing needs. However, before deviating from the steps in this QuickStart, be sure to review the limitations listed below for the corresponding feature to avoid any confusion.


## Scenarios
Here are a few scenarios you can try out.  Please refer the details below on the limitations.  Each scenario is segregated by it's own namespace to keep the testing clean and simple.  However, you can tweak the scenarios to configure all the resources under same namespace for testing further.

| # | Scenario | Description |
| ------------ | ------------ | ------------ |
| 1 | Fan-out (one-to-many) messages  | This scenario simulates cloud-to-client commands to several clients and can be leveraged for use cases such as sending alerts to clients. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet. For instructions see [README](/Scenario1_Fan-out%20messages/README.md).  |
| 2 | Fan-in (many to one) messaging  | This scenario simulates publishing messages from multiple clients to a single client.  Consider a use case where one needs to identify location of vehicles on a map.  For instructions see [README](/Scenario2_Fan-in%20(many%20to%20one)%20messaging/README). |
| 3 | One to one messaging  | This scenario simulates publishing messages from one client to another.  Consider a use case where a user can unlock their car from a mobile app.  For instructions see [README](/Scenario3_One%20to%20one%20messaging/README.md).  |
| 4 | Route MQTT data through Event Grid subscription  | This scenario showcases how to configure route to send filtered messages from broker to the endpoint: Kafka on Event Hub through EG subscription.  Consider a use case where one needs to identify location of vehicles.  For instructions see [README](/Scenario4_Route%20MQTT%20data%20through%20Event%20Grid%20subscription/README.md).  |


## Terminology
Some of the key terms relevant for private preview are explained below.

| Term| Definition |
| ------------ | ------------ |
| MQTT Broker| An MQTT broker is an intermediary entity that enables MQTT clients to communicate. Specifically, an MQTT broker receives messages published by clients, filters the messages by topic, and distributes them to subscribers. |
| Namespace| A namespace is a declarative region that provides a scope to the resources (certificates, clients, client groups, topicspaces, permissionbindings, etc.) inside it.  Namespaces are used to organize the resources into logical groups. |
| Client| Client can be a device or a service that will publish and/or subscribe MQTT messages |
| Certificate / Cert| Certificate is a form of asymmetric credential. They are a combination of a public key from an asymmetric keypair and a set of metadata describing the valid uses of the keypair.  If the keypair of the issuer is the same keypair as the certificate, the certificate is said to be “self-signed”. Third-party certificate issuers are sometimes called Certificate Authorities (CA). |
| Client attributes| Client attributes represent a set of key-value pairs that provide descriptive information about the client.  Client attributes are used in creating client groups and as variables in Topic Templates.   For example, Floor 3 is an attribute that provides the client's location. |
| Client group| Client group is a collection of clients that are grouped by a set of common client attribute(s) using a query string, and will publish and/or subscribe to a specific Topic Space |
| Topic space | Topic space is a set of topic templates (defined below). It is used to simplify access control management by enabling you to grant publish or subscribe access to a group of topics at once instead of individual topics. |
| Topic filter| An MQTT topic filter is an MQTT topic that can include wildcards for one or more of its segments, allowing it to match multiple MQTT topics. It is used to simplify subscriptions declarations as one topic filter can match multiple topics. |
| Topic template| Topic templates are an extension of the topic filter that supports variables. It is used for fine-grained access control within a client group. |
| PermissionBinding| A Permission Binding grants access to a specific client group to either publish or subscribe on a specific topic space.  |

## Concepts

### Client Authentication
For private preview, we will be supporting authentication of clients using X.509 certificates.  X.509 certificate will provide the credentials to associate a particular client with the tenant, and at the same time, ensure the communication is encrypted.  In this model, authentication generally happens once during session establishment.  Then, all future operations using the same session are assumed to come from that identity. 
The following credential types are supported:
- Certificates issued by a Certificate Authority (CA) 
- Self-signed certificates

**CA signed certificates:**  In this method, a root or intermediate X.509 certificate is registered with the service.  Later, clients can authenticate if they have a valid leaf certificate that's derived from the root or intermediate certificate.  While registering the clients, the subject common name of the leaf certificate needs to be supplied for authentication.  Service will validate the subject name with the CA certificate that was registered earlier to validate the identity of the client.  

**Self-signed certificates:**  For self-signed certificates, clients are onboarded to the service using the  certificate thumbprint alongside the identity record.  In this method of authentication, the client registry will store the exact ID of the certificate that the client is going to use to authenticate. 


### Client Groups
Client group is a new concept introduced to make management of client access controls (publish/subscribe) easy – multiple clients can be grouped together based on certain commonalities to provide similar levels of authorization to publish and/or subscribe to Topic spaces.

Clients can be devices or applications, such as devices or vehicles that send/receive MQTT messages.

For example, a fleet management company with hundreds of trucks and other shipment delivery vehicles across the country, can improve their routing, tracking, driver safety and predictable maintenance capabilities by sending and receiving MQTT messages to/from the vehicles to monitoring applications on cloud.

In this scenario, vehicles can be configured as clients that publish/subscribe to various topics such as weather information, road conditions, geo location, engine performance and other wear-and-tear aspects of the vehicle.  And, while configuring the vehicle as a client, a set of attributes such as vehicle type, year, make & model, max load capacity can also be included as part of the client metadata.

These client attributes can be used to create the client groups.  For example, if the vehicles that can carry loads over 2 tons are prone to accidents if driven with low braking fluid especially in icy road conditions, then all such vehicles can be grouped together to continuously monitor and alert the drivers in case of potential hazardous conditions based on weather at their locations.

### Client group considerations:
The main purpose of client groups is to provide common authorization to a set of clients to either publish and/or subscribe on one or more Topic spaces.  Every client needs to be part of a client group to be able to pub/sub on a topic space.  The goal is to keep the quantity of client groups very small to make permissions manageable.
For this preview, we will be supporting a maximum of 10 client groups per namespace.

Clients need to be grouped in a way that it’s easier to reuse the group to pub/sub across multiple topic spaces.  To this end, it is important to think through the end-to-end scenarios to identify the topics every client will publish/subscribe to.  Identify the commonalities across the scenarios to avoid over fragmentation of client groups and topic spaces.  Set the client attributes generic enough to achieve simple grouping and avoid highly complex group queries.

**What are client attributes?**
Client attributes are a set of user defined key-value pairs or tags that provide information about the client.  These attributes will be the main ingredient in the client group filtering expressions.  Attributes could be describing the physical or functional characteristics of the client.  Typical attributes could be type of the client, client location, or type of signal generated from the client.  
Here are some examples of typical client attributes:
- Type: Values could be “sensor” or “thermostat” or “vehicle”
- Client location could be a plant, particular geo, or a state

Here’s a sample schema for the attribute definition: 

```json
{  
    "id": "device123",  
    "attributes": {  
        "floor": 7,  
        "status": “active”,  
        "sensors": ["motion", "noise", "light"]  
     }  
}
```

While configuring the client attributes, consider the topics that the clients will be publishing (subscribing) to.  Thinking backwards from topics to clients will help identifying the commonalities across client roles much easier and defining the client attributes to make the client grouping effortless.  

**How to create client group queries?**
To setup a client group, user needs to build a query that filters a set of clients based on their attribute values.

Here are a few sample queries:
- (Attributes.sensors = “motion” or Attributes.sensors = “humidity”) or Attributes.status <> “sleep mode”
- Attributes.sensors IN [“motion”, “humidity”, “temperature”] and attributes.floor <= 5

In group queries, following operands are allowed:
- Equal operator “=”
- Not equal operator in 2 forms “<>” and “!=” 
- Less than “<”, greater than “>”, less than equal to “<=”, greater than equal to “>=” for long integer values
- “IN” to compare with a set of values

Please refer to the [naming considerations table](#naming-considerations) for details on allowed characters and patterns.


### Topic Spaces
Topic space is a new concept introduced to simplify management of topics used for publishing and subscribing by your clients.

**Topic space:**  A topic space is a set of topic templates (defined below). It is used to simplify access control management by enabling you to grant publish or subscribe access to a group of topics at once instead of individual topics.  
It is important to note that the publishing is a supported action on all topic spaces by default; however, you need to configure the subscription support as detailed below.

**Topic filter:**  An [MQTT topic filter](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718106) is an MQTT topic that can include wildcards for one or more of its segments, allowing it to match multiple MQTT topics. It is used to simplify subscriptions declarations as one topic filter can match multiple topics.

The service supports all the MQTT wildcards defined by the [MQTT specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718107) as follows:
- +: which matches a single segment.
	- E.g. topic filter: “machines/+/alert” will match the following topics:
		- machines/temp/alert
		- vehicles/humidity/alert
- #: which matches zero or more segments at the end of the topic. 
	- E.g. topic filter: “machines/#” will match the following topics:
		- machines
		- machines/temp
		- machines/humidity
		- machines/temp/alert etc

See [Topic Wilcards](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718107) from the MQTT spec for more details.

**Topic template:** Topic templates are an extension of the topic filter that supports variables. It is used for fine-grained access control within a client group. You can provide access to a client group to publish or subscribe on a topic space with multiple topic templates. If any of the topic templates include a variable, only the clients associated with this variable will have access to the corresponding topic.

For example, you can provide access to client group “machines” to the topic space “machinesTelemetry” that includes the topic template “machines/${client.name}/temp”. Only the machine with client name = machine1 will be able to publish on topic “machines/machine1/temp”, and only the machine with client name = machine2 will be able to publish on topic “machines/machine2/temp”, and so on. This prevents machine2 from publishing false information on behalf of machine1, even though it has access to the same topic space, and vice versa. 

**Supported variables:**
- ${client_name}: this variable represents the name of the client assigned during client creation.
- ${client.attributes.x}: this variable represents any of the assigned attributes to a client during client creation/update, so as “x” would be equal to the exact string of the attribute key. Read more about client attributes in the Terminology section.

**Note:** A variable can represent a portion of a segment or an entire segment but cannot cover more than one segment. E.g. a topic template could include “machines/${client.name|.factory1}/temp” will match topics “machines/machine1.factory1/temp”, “machines/machine2.factory1/temp”, etc

**Subscription support:** Subscription support is used to optimize the service’s mode of  message delivery to your clients based on your scenario. There are three modes: 
- Not supported: will indicate that topic space could be used only for publishing. This will be helpful in scenarios when you expect your corresponding topic templates to overlap since this is the only mode that will allow your topic templates to overlap with any other topic template.
- Low fanout: will specify a subscription delivery mode optimized for having a maximum of 10 subscribers per topic, with very low latency. 
	- Example scenario: There is a group of vehicles with each vehicle subscribing to its own command delivered to its own topic.
- High fanout: will specify a subscription delivery mode optimized for having unlimited number of subscribers per topic, with higher latency.
	- Example scenario: There is a large group of vehicles in a city subscribing to the same weather alerts that get broadcasted on the same topic.

### Topic space considerations
- **Default Behavior:**
To publish or subscribe to any topic, a matching topic space must be configured, and a permission binding needs to be set for the client group(s) that include the clients that need publish/subscribe access to this topic space. 
- **Topic templates Overlap:**
If you set your topic space with a low fanout or high fanout subscription modes, the corresponding topic templates cannot overlap with each other, but they can overlap with a topic space with “not supported” subscription support. The overlap exists if a topic could match more than one topic template: 
	- Examples:
		- “machines/${client.name}/temp” and “machines/+/temp” /#” overlap because the second template covers the first one via wildcard. 
		- vehicles/vehicle1/telemetry/# and vehicles/${principal.deviceId}/telemetry/# conflict because in the second template the segment with variable is treated as single level wildcard + and hence, covers the first topic template. PublishOnly topic spaces can overlap with LowFanout topic spaces.
- **Configuration:**
	- Topic templates use special characters $ and | and these need to be escaped differently based on the shell being used. In PowerShell, $ can be escaped with vehicles/${dollar}telemetry/#. If you’re using PowerShell, you can accomplish this as shown in the examples below: 
		- '"vehicles/${principal.deviceId|dollar}/#"'
		- 'vehicles/${principal.deviceId"|"dollar}/#'
	- Subscription support is immutable. To reconfigure the subscription support, delete the topic space and create a new topic space with the desired subscription support.
	- Topic space updates may take up to 5 minutes to propagate.


### Access Controls

Grouping Clients into Client Groups and Topic Templates into Topic Spaces is designed to simplify access control. Consider the following as you design Client Groups and Topic Spaces: 
- Group Clients within Client Groups such that each Client Group represents Clients that need the same access to publish and/or subscribe to the same set of topics.
- Group Topic Templates within Topic Spaces such that each Topic Space represents messages meant for the same audience (group of clients).

For example:
- Example 1:

    A factory has multiple sections with each section including Clients that need to communicate with each other. However, Clients from other sections of the factory are not allowed to communicate with them.


| Client  | Role  | Topic/Topic Filter  |
| ------------ | ------------ | ------------ |
|Section1_Client1| Publisher| sections/section1/clients/client1|
|Section1_Client2| Subscriber| sections/section1/clients/#|
|Section2_Client1| Publisher| sections/section2/clients/client1|
|Section2_Client2| Subscriber| sections/section2/clients/#|

- Configuration
	- Create a Client Group for each factory section’s clients.
	- Create a Topic Space for each section representing the topics that the section’s clients will communicate over.
	- Create 2 Permission Bindings for each section’s Client Group to publish and subscribe to its corresponding section’s Topic Space.

|Client| Client Group| Permission Binding| Topic Space|
| ------------ | ------------ | ------------ | ------------ |
|Section1_Client1| Section1Clients| Section1-Pub| Section1Messages -Topic Template: sections/section1/clients/#|
|Section1_Client2|Section1Clients | Section1-Sub| Section1Messages -Topic Template: sections/section1/clients/#|
|Section2_Client1| Section2Clients| Section2-Pub| Section2Messages -Topic Template: sections/section2/clients/#|
|Section2_Client2|Section2Clients | Section2-Sub| Section2Messages -Topic Template: sections/section2/clients/#|

- Example 2:

    Let’s assume an extra requirement for the example above: each section has management clients and operator clients, and the operator clients must not have publish access in case any of them gets compromised. On the other hand, the management clients need publish access to send commands and subscribe access to receive telemetry.

| Client | Role | Topic/Topic Filter | 
| ------------ | ------------ | ------------ |
| Section1_OperatorClient1 | Publisher | sections/section1/OpClients/client1
|| Subscriber | sections/section1/MgmtClients/# | 
| Section1_MgmtClient1 | Publisher | sections/section1/MgmtClients/client1
|| Subscriber | sections/section1/OpClients/# | 
 | Section2_OperatorClient1 | Publisher | sections/section2/OpClients/client1
| |Subscriber | sections/section2/MgmtClients/# | 
| Section2_ MgmtClient1 | Publisher | sections/section2/MgmtClients/client1 | 
||Subscriber | sections/section2/OpClients/# |

- Configuration:
	- Create 2 Client Groups per section: one for the management clients and another for the operator clients.
	- Create 2 Topic Spaces for each section: one representing telemetry topics and another representing commands topics.
	- Create 2 Permission Bindings for each section’s management clients to publish to the commands Topic Space and subscribe to the telemetry Topic Space.
	- Create 2 Permission Bindings for each section’s operator clients to subscribe to the commands Topic Space and publish to the telemetry Topic Space.


|Client | Client Group | Permission Binding | Topic/Topic Filter|
| ------------ | ------------ | ------------ | ------------ |
|Section1_OperatorClient1 | Section1Operators | Section1Op-Pub | Section1Telemetry -Topic Template: sections/section1/OpClients/#|
| |  | Section1Op-Sub | Section1Commands -Topic Template: sections/section1/MgmtClients/#|
|Section1_MgmtClient1 | Section1Mgmt | Section1Mgmt-Pub | Section1Commands -Topic Template: sections/section1/MgmtClients/#|
| |  | Section1Mgmt-Sub | Section1Telemetry -Topic Template: sections/section1/OpClients/#|
|Section2_OperatorClient1 | Section2Operators | Section2Op-Pub | Section2Telemetry -Topic Template: sections/section2/OpClients/#|
| |  | Section2Op-Sub | Section2Commands -Topic Template: sections/section2/MgmtClients/#|
|Section2_ MgmtClient1 | Section2Mgmt | Section2Mgmt-Pub | Section2Commands -Topic Template: sections/section2/MgmtClients/#|
| |  | Section2Mgmt-Sub | Section2Telemetry -Topic Template: sections/section2/OpClients/#|
 




### Routing
This functionality will enable you to route your messages from your clients to different Azure services like Event hubs, Service Bus, etc or your custom endpoint. This functionality is achieved through [Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/), by sending all your messages from your clients to an [Event Grid topic](https://docs.microsoft.com/en-us/azure/event-grid/custom-topics), and using [Event Grid subscriptions](https://docs.microsoft.com/en-us/azure/event-grid/subscribe-through-portal) to route the messages from that Event Grid topic to the [supported endpoints](https://docs.microsoft.com/en-us/azure/event-grid/event-handlers).

Event Grid is a highly scalable, serverless event broker that you can use to integrate applications using events. Events are delivered by Event Grid to subscriber destinations such as applications, Azure services, or any endpoint to which Event Grid has network access. [Learn more](https://docs.microsoft.com/en-us/azure/event-grid/)

**Note:**  To be able to take advantage of this feature, you have to either use the ARM template to create the Event Grid custom topic first and provide that topic’s ARM Id during the namespace creation.

### High-Level Steps
You can either use the X ARM template to create the Event Grid custom topic as well as the namespace or create your Event Grid custom topic as the first step to route your messages.

**Using the ARM template:**
1. Use the ARM template to create the [Event Grid topic](https://docs.microsoft.com/en-us/azure/event-grid/custom-topics) as well as the namespace. The created custom topic is where all MQTT messages will be forwarded.
2. Create an [Event Grid subscription](https://docs.microsoft.com/en-us/azure/event-grid/subscribe-through-portal) to route these messages to one of the supported Azure services or a custom endpoint.

**Create your Event Grid custom topic:**
1. [Create an Event Grid custom topic](https://docs.microsoft.com/en-us/azure/event-grid/custom-event-quickstart-portal) where all MQTT messages will be forwarded. This topic needs to fulfill the requirements detailed below in the routing considerations.
2. Create an [Event Grid subscription](https://docs.microsoft.com/en-us/azure/event-grid/subscribe-through-portal) to route these messages to one of the supported Azure services or a custom endpoint.
3. Create the namespace with MQTT Enabled and pass on the ARM ID for the custom topic that you created in step 1.

### Routing Considerations:
- The Event grid topic that will be used for routing need to fulfil the following requirements:
- It needs to be set to use the Cloud Event Schema v1.0
- It needs to be in the same region as the namespace
- **Filtering:**
	- You can use the Event Grid Subscription’s filtering capability to filter the routed messages based on the MQTT topic through filtering on the “subject” property in the Cloud Event schema. Event Grid Subscriptions supports free simple subject filtering by specifying a starting or ending value for the subject. For example, 
		- You can specify the subject ends with “gps” to only route messages reporting on location. 
		- You can filter the subject begins with “factory1/Area2/” to route only the messages that belong to facotry1 and area 2 to a specific endpoint and you can replicate this configuration to route messages from other factories/areas to different endpoints.
	- You can also take advantage of the [Event Subscription’s advanced filtering](https://docs.microsoft.com/en-us/azure/event-grid/event-filtering#advanced-filtering) to filter based on the MQTT topic through filtering on the subject property in the Cloud Event Schema. This enable you to set more complex filters by secifying a comparison operator, key, and value. See the example below.

#### The schema for the Cloud Event Schema:
Each message being routed is enveloped in a Cloud Event according to the following schema sample: 
```json
{
    "specversion": "1.0",
    "id": "9aeb0fdf-c01e-0131-0922-9eb54906e20", // Unique id generated by the gateway upon receiving the message
    "time" : "2019-11-18T15:13:39.4589254Z", // time of message arriving to Azure pub-sub assigned by gateway
    "type" : "MQTT.EventPublished",
    "source"  : "namespace1", // name of your namespace that received the MQTT message.
    "subject" : "vehicles/ floor1/ vehicleId1/temp" , //MQTT topic that accompanied the MQTT publish message.   
  "data" : “<Published MQTT message>”
}
```

## Limits
For this release, the following limits are supported.  Please do not stress test beyond the limits mentioned below and for other scenarios.  These limits will be revised for future releases.

|Limit Description | MQTT Private Preview |
| ------------ | ------------ |
|Max Message size | 256KB |
|Topic Size| 256KB - is this accurate? | 
|New Connect requests | 500/second per namespace |
|Subscribe requests | 5000 messages/second |
|Total number of subscriptions per connection | 50 |
|Total inbound publish requests | 5000 messages/second per namespace |
|Total inbound Publish requests per connection | 100/second |

### Resources level limits
| Resource Type | Description| Limit| 
| ------------ | ------------ | ------------ |
| Name spaces | Maximum number of name spaces per subscription | 10 |
| Clients | Maximum number of clients | 10K |
| CA Certificates | Maximum number of registered CA root certificates | 2 |
| Client Groups | Number of client groups per namespace | 10 |
| Topic spaces | Maximum number of topic spaces | 10 |
| Topic templates | Maximum number of topic templates within a topic space | 10 |
| Permission bindings | Maximum number of permission bindings | 100 |

## Naming considerations
All the names are of String type

| Category| Name length| Allowed characters| Other considerations|
| ------------ | ------------ | ------------ | ------------ |
| Namespace| 6-50 characters| Alphanumeric, and hyphens(-); no spaces|  Starts with letter and ends with alphanumeric; Name needs to be unique per region | 
|CA Certificate| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| Name needs to be unique per namespace | 
| Client| 1-128 characters| Alphanumeric, hyphen(-), colon(:), dot(.), and underscore(_), no spaces| Case sensitive; Name needs to be unique per namespace | 
| Client attributes| Total size of the attributes is <=4KB| Alphanumeric and underscores(_)| Case sensitive; Attribute values can be strings, string arrays, integers; Name needs to be unique per namespace| 
| Client Group| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| $all is the default client group that includes all the clients.  This group cannot be edited or deleted; Name needs to be unique per namespace| 
| TopicSpace| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| |
| Permission Bindings| 3-50 characters| Alphanumeric, hyphen(-) and, no spaces| Name needs to be unique per namespace | 

## Frequently asked questions 
- Is monitoring metrics and logging available? 
	- Not in this release.  We will add monitoring metrics and diagnostic logs in the next release.
- What happens if client attempts to pub/sub on a topic when a matching topic space is not found? 
	- Client connection will be closed. 
- How long does it take for topic space updates to propagate? 
	- It takes up-to 5 minutes to propagate a topic space update. 
- How can my clients send MQTT messages to the service? 
	- You can use any standard MQTT client SDK.  See SDK samples here. 
- How can I fix Subscription was rejected error when running the samples? 
	- Topic space updates take up-to 5 minutes to propagate, please retry the samples post that. 
- How do I connect to the MQTT feature with a third party tool that requires username and password as string? 
	- Username and password based authentication is currently not supported.  It will be supported in future release.
- What happens if I have more than 10 subscribers per topic for a low fanout topic space?
    - The 11th subscription request for the same topic will be rejected.
- Is MQTT 3.1 supported?
    - No



