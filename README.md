# Customer onboarding instructions - MQTT Broker Private Preview

The Microsoft Azure messaging team invites you and your organization to preview the MQTT Broker feature.  During this preview, we will provide full support with a high level of engagement from the Azure messaging product group. We look forward to your feedback  as you leverage this capability for your pub/sub solutions. Please note that this preview is available by invitation only  and requires an NDA. By participating in the private preview, you agree to the [Terms of Use](https://www.microsoft.com/legal/terms-of-use).

## Overview of MQTT Broker
MQTT broker is a pub/sub messaging broker, to enable secure transfer of messages to and from IoT  clients and applications. You can now use MQTT’s flexible topic structure to send and receive messages from your clients (clients/services) and support flexible messaging patterns such as command and control and as well as broadcast messages to clients (clients/services).

## Private preview program information
The private preview is only for testing.  Please do NOT use it for your production.

**Engagement:**  We will actively engage with you during the preview. At any point, feel free to connect with us for questions/concerns by creating issues in the Samples repo, confidential questions can be asked to mqttbroker@microsoft.com.

**Feedback:**  At the end of the preview, we will capture additional feedback using this form.

**Cost to use:**  For this release, MQTT Broker is available for no additional charge. You will be charged for routing MQTT messages through Event Grid subscriptions (https://azure.microsoft.com/en-us/pricing/details/event-grid/).

## Post private preview program
When the private preview program ends, or when your tests are complete, we will provision to migrate all the MQTT brokers and corresponding data to public preview.

However, if you prefer to cleanup the private preview configuration, you can follow these below steps.

## Capabilities  available in this preview
This private preview provides the following capabilities

**MQTT Broker functionality** in Canary via APIs.
- Cloud MQTT Broker with pub/sub to flexible topic structure, support wildcards in topic structure to allow subscription to filtered messages
- MQTT v3.1.1. compliance with limitations (LWT, Retain messages, Message ordering and QoS 2 not supported) 
- QoS 0, 1 - MQTT manages the re-transmission of messages and guarantees delivery making communication in unreliable networks a lot reliable.
- Fine grained access control on pub/sub, means users can configure precisely for specific clients to pub/sub on specific topics level
- Compatibility with standard MQTT client libraries (ex. Eclipse Paho) allows users to migrate configuration much faster
- Route MQTT messages through Event Grid subscriptions to integrate data with Azure services  for flexibility to further process the data on various Azure endpoints
- Persistent session will allow for clean session if client disconnects and reconnects, ensuring subscribed messages are sent after reconnection.
- High fan out/broadcasting to large number of subscribers on each topic  
- Support for 1-1, 1-many and many-1 messaging patterns to accommodate for a variety of pub/sub scenarios
- Client (client/service)  onboarding and authentication using X.509 certificates
- Ability for registered clients to publish or subscribe to any topic through client groups
- Topic Spaces is a new concept introduced to simplify management of topics used for pub/sub  
- Support for TLS 1.2   endpoints for data plane operations to keep the data transmission secure
- See throttle limits table below
## Capabilities coming up in future releases
- Last Will and Testament (LWT)
- Retain flag
- Azure Portal UX, CLI, custom Azure SDK libraries apart with APIs
- Enhanced performance and scale limits
- MQTT v5 (partial)
- Customer facing Azure monitoring metrics, Azure diagnostic logs for troubleshooting and monitoring operations
- Large message of 1MB  supported 
- Pay As You Go Billing


## Concepts
||
| ------------ |
| [MQTT standard protocol](https://mqtt.org/) |
| Client Authentication(#Client Authentication) |
| Client Groups |
| Topic Space |

### Client Authentication
In the context of an identity-based access control system, authentication is the process of verifying an identity. Authentication occurs by the client proving to the server that it possesses the secret data/credential, which links to it’s identity via a trusted channel.  To authenticate the identity, the client proves possession of the credential, and through the transitive property, its identity.
In MQTT systems using an identity-based access control model, authentication generally happens once during session establishment.  Then, all future operations using the same session are assumed to come from that identity.
The following credential types are currently supported:
- Certificates issued by a Certificate Authority (CA) – asymmetric
- Self-signed certificates - asymmetric

**Certificates:** Certificates, are a form of asymmetric credential.  They are a combination of a public key from an asymmetric keypair and a set of metadata describing the valid uses of the keypair. 
For asymmetric keypair based authentication, the identity registry must store the identity’s public key alongside the identity record so that it can verify tokens sent by the client and signed with the private key.

**CA signed certificates:**  For trusted issuer certificates (CA signed), the identity registry only needs to store the list of trusted issuers and the public keys that these issuers use to sign certificates.  The link between credential and identity is not stored in the identity registry but is embedded in the certificate itself.  Because the metadata can be trusted by verifying the certificate issuer, the identity registry can trust the identity listed in the subject field and does not need to store any additional information about the credentials.
In this method, a root or intermediate X.509 certificate is registered with the service.  Later, clients can authenticate if they have a valid leaf certificate that's derived from the root or intermediate certificate.

**Self-signed certificates:**  For self-signed certificates, the identity registry must store either the identity certificate’s public key or the identity’s certificate thumbprint alongside the identity record.  The certificate thumbprint is a cryptographic hash of the certificate data (public key and metadata).  The identity registry needs to store the exact ID of the certificate that the client is going to use to authenticate. 

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

### Routing
This functionality will enable you to route your messages from your clients to different Azure services like Event hubs, Service Bus, etc or your custom endpoint. This functionality is achieved through [Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/), by sending all your messages from your clients to an [Event Grid topic](https://docs.microsoft.com/en-us/azure/event-grid/custom-topics), and using [Event Grid subscriptions](https://docs.microsoft.com/en-us/azure/event-grid/subscribe-through-portal) to route the messages from that Event Grid topic to the [supported endpoints](https://docs.microsoft.com/en-us/azure/event-grid/event-handlers).

Event Grid is a highly scalable, serverless event broker that you can use to integrate applications using events. Events are delivered by Event Grid to subscriber destinations such as applications, Azure services, or any endpoint to which Event Grid has network access. [Learn more](https://docs.microsoft.com/en-us/azure/event-grid/)

**Note:**  To be able to take advantage of this feature, you have to either use the ARM template to create the Event Grid custom topic first and provide that topic’s ARM Id during the namespace creation.

### High-Level Steps
You can either use the X ARM template to create the Event Grid custom topic as well as the namespace or create your Event Grid custom topic as the first step to route your messages.

**Using the ARM template:**
1. Use the ARM template to create the Event Grid topic as well as the namespace. The created custom topic is where all MQTT Broker messages will be forwarded.
2. Create an Event Grid subscription to route these messages to one of the supported Azure services or a custom endpoint.

**Create your Event Grid custom topic:**
1. [Create an Event Grid custom topic](https://docs.microsoft.com/en-us/azure/event-grid/custom-event-quickstart-portal) where all MQTT Broker messages will be forwarded. This topic needs to fulfill the requirements detailed below in the routing considerations.
2. Create an Event Grid subscription to route these messages to one of the supported Azure services or a custom endpoint.
3. Create the namespace with MQTT Enabled and pass on the ARM ID for the custom topic that you created in step 1.

### Routing Considerations:
- The Event grid topic that will be used for routing need to fulfil the following requirements:
- It needs to be set to use the Cloud Event Schema v1.0
- It needs to be in the same region as the namespace
- **Filtering:**
	- You can use the Event Grid Subscription’s filtering capability to filter the routed messages based on the MQTT topic through filtering on the “subject” property in the Cloud Event schema. Event Grid Subscriptions supports free simple subject filtering by specifying a starting or ending value for the subject. For example, 
		- You can specify the subject ends with “gps” to only route messages reporting on location. 
		- You can filter the subject begins with “factory1/Area2/” to route only the messages that belong to facotry1 and area 2 to a specific endpoint and you can replicate this configuration to route messages from other factories/areas to different endpoints.
	- You can also take advantage of the Event Subscription’s advanced filtering to filter based on the MQTT topic through filtering on the subject property in the Cloud Event Schema. This enable you to set more complex filters by secifying a comparison operator, key, and value. See the example below.

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
For this release, the following limits are supported, however, not all limits are enforced, please do not stress test beyond the limits mentioned above.  The limits might be revised for future releases.


