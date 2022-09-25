# Scenario 1 – Fan-out (one-to-many) messages
This scenario simulates cloud-to-device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alerts to all the vehicles in the fleet.

|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|fleet_mgt_client (Attributes: “Type”:”Fleet_Mgmt”)| FleetMgmt| FleetMgmt-publisher|  WeatherAlerts (Topic template: fleet/alerts/weather/alert1)|
|vehicle1 (Attributes: “Type”:”Vehicle”)| Vehicles| Vehicles-subscriber|  WeatherAlerts (Topic template: fleet/alerts/#)|
|vehicle2 (Attributes: “Type”:”Vehicle”)| Vehicles| Vehicles-subscriber|  WeatherAlerts (Topic template: fleet/alerts/#)|


**Instructions:**

- Download the folder Scenario1_jsons with JSON files to C:
- Create the namespace under the resource group that you already created as part of the prerequisites.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS --is-full-object --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\NS_Scenario1.json
```

If you are using a CA certificate to authenticate the clients, the encoded certificate string must be in valid PEM (Privacy Enhanced Mail) format with header (-----BEGIN CERTIFICATE-----) and footer (-----END CERTIFICATE-----). This string must not include a private key. Save the certificate as a json file named MqttCACertificate.json in C:\Scenario1_jsons\ folder.  You can include a description in the properties as below.

```json
{
    "properties":{
   	  "description": "This is a test certificate",
        "encodedCertificate": "-----BEGIN CERTIFICATE-----

 -----END CERTIFICATE-----"
    }
}
```

Register the CA Certificate using the below command.  Replace the \<Subscription ID\> with your subscription ID.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/caCertificates --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/caCertificates/CACert --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\MqttCACertificate.json
```

Onboard the Clients using below CLI commands.

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/clients/fleet_mgt_client --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\C_fleet_mgt_client.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/clients/vehicle1 --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\C_vehicle1.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clients --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/clients/vehicle2 --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\C_vehicle2.json
```

Create the Client Groups using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/clientGroups/FleetMgmt --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\CG_FleetMgmt.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/clientGroups --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/clientGroups/Vehicles --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\CG_FleetMgmt.json
```

Create the Topic Spaces using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/topicSpaces --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/topicSpaces/WeatherAlerts --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\TS_WeatherAlerts.json
```

Create the Permission Bindings using below CLI commands

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/permissionBindings/FleetMgmt-publisher --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\PB_FleetMgmt-publisher.json
```

```bash
az resource create --resource-type Microsoft.EventGrid/namespaces/permissionBindings --id /subscriptions/<Subscription ID>/resourceGroups/MQTT-Pri-Prev-rg1/providers/Microsoft.EventGrid/namespaces/Scenario1-NS/permissionBindings/Vehicles-subscriber --api-version 2022-10-15-preview --properties @C:\Scenario1_jsons\PB_Vehicles-subscriber.json
```

