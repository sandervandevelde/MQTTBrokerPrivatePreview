# Scenario 2 – Fan-in (many to one) messaging
This scenario simulates device to cloud communication and can be leveraged for use cases such as sending telemetry to the backend service. Consider a use case where the backend service needs to identify the location of vehicles on a map. Vehicles should be prohibited from listening to other vehicles’ locations or publishing other vehicles’ location on their behalf.

**Scenario:**

|Client | Role | Topic/Topic Filter|
| ------------ | ------------ | ------------ |
|s2-map-client | Subscriber | vehicles/+/GPS/position |
|s2-vehicle1 | Publisher | vehicles/vehicle1/GPS/position |
|s2-vehicle2 | Publisher | vehicles/vehicle2/GPS/position |

**Resource Configuration:**
|Client| Client Group| PermissionBinding (Role)| TopicSpaces|
| ------------ | ------------ | ------------ | ------------ |
|s2-map-client (Attributes: “Type”:”Mapping”)| map | map-subscriber |  subscribe: -Topic Templates: vehicles/+/GPS/position -Subscription Support: LowFanout |
|s2-vehicle1 (Attributes: “Type”:”Vehicle”)| vehicles| vehicles-publisher |  publish: -Topic Templates: vehicles/${client.name}/GPS/position -Subscription Support: NotSupported |
|s2-vehicle2 (Attributes: “Type”:”Vehicle”)| Vehicles| vehicles-publisher |  publish: -Topic Templates: vehicles/${client.name}/GPS/position -Subscription Support: NotSupported |

Follow the instructions in the [Prerequisites](#prerequisites) to test this scenarios. You can either configure these resources through the script or manually. Afterwards, test the scenario using the python script to observe the data flow.

**Configure the resources through the script:**
- Run the following commands to run the script, creating the resources: 
```bash
chmod 700 create_resources.sh
./create_resources.sh
```

**Configure the resources manually:**
- Create a namespace:
```bash
az resource create --resource-type ${base_type} --id ${resource_prefix} --is-full-object --api-version 2022-10-15-preview --properties @./resources/NS_Scenario2.json
```
- Generate certificates using the cert-gen scripts. You can skip this step if you're using your own certificate.
```bash
pushd ../cert-gen
./certGen.sh create_leaf_certificate_from_intermediate s2-vehicle1
./certGen.sh create_leaf_certificate_from_intermediate s2-vehicle2
./certGen.sh create_leaf_certificate_from_intermediate s2-map-client
popd
```
- Create the CA Certificate:
```bash
az resource create --resource-type ${base_type}/caCertificates --id ${resource_prefix}/caCertificates/test-ca-cert --api-version 2022-10-15-preview --properties @./resources/CAC_test-ca-cert.json
```
- Register the following clients:
	- s2-map-client
		- Attribute: Type=mapping
	- s2-vehicle1
		- Attribute: Type=vehicle
	- s2-vehicle2
		- Attribute: Type=vehicle
```bash
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s2-map-client --api-version 2022-10-15-preview --properties @./resources/C_map-client.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s2-vehicle1 --api-version 2022-10-15-preview --properties @./resources/C_vehicle1.json
az resource create --resource-type ${base_type}/clients --id ${resource_prefix}/clients/s2-vehicle2 --api-version 2022-10-15-preview --properties @./resources/C_vehicle2.json
```
- Create the following client groups:
	- map to include the s2-map-client
		- Query: ${client.attribute.Type}= “mapping”
	- vehicles to include s2-vehicle1 and s2-vehicle2 clients
		- Query: ${client.attribute.Type}= “vehicle”
```bash
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/map --api-version 2022-10-15-preview --properties @./resources/CG_map.json
az resource create --resource-type ${base_type}/clientGroups --id ${resource_prefix}/clientGroups/vehicles --api-version 2022-10-15-preview --properties @./resources/CG_vehicles.json
```
- Create the following topic spaces:
	- subscribe:
		- Topic Templates: vehicles/+/GPS
		- Subscription Support: LowFanout
	- publish:
		- Topic Templates: vehicles/${client.name}/GPS
		- Subscription Support: NotSupported
```bash
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/subscribe --api-version 2022-10-15-preview --properties @./resources/TS_subscribe.json
az resource create --resource-type ${base_type}/topicSpaces --id ${resource_prefix}/topicSpaces/publish --api-version 2022-10-15-preview --properties @./resources/TS_publish.json
```

- Create the following permission bindings:
	- map-subscriber: to grant access for the client group map to subscribe to the topic space subscribe
	- vehicles-publisher: to grant access for the client group vehicles to publish to the topic space publish
```bash
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/map-subscriber --api-version 2022-10-15-preview --properties @./resources/PB_map-subscriber.json
az resource create --resource-type ${base_type}/permissionBindings --id ${resource_prefix}/permissionBindings/vehicles-publisher --api-version 2022-10-15-preview --properties @./resources/PB_vehicles-publisher.json
```
**Test the scenario using the python scripts:**
1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open two terminal windows in your Linux environment, and run the following commands in both terminal windows after editing the \<namespace name>:
```bash
# Make sure you have the `mqtt-broker` virtual environment activated 
source ~/env/mqtt-broker/bin/activate
# Set up the following variable
export gw_url="<namespace name>.centraluseuap-1.ts.eventgrid.azure.net"
```
3. In one terminal window, run the subscribe sample script through the following command: `python ./subscribe.py`.
4. In the other terminal window, run the publish sample script through the following command: `python ./publish.py`.
5. Observe the messages in the published messages in the subscribe terminal window.
