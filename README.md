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


|  Concepts |
| ------------ |
| [MQTT standard protocol](https://mqtt.org/) |
| Client Authentication |
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


