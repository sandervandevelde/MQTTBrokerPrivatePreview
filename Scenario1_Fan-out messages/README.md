# Scenario 1 – Fan-out (one-to-many) messages
This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet.


|Client name|Client Group|PermissionBinding|TopicSpace|Topic template|
| ------------ | ------------ | ------------ | ------------ | ------------ |
|fleet_mgt_client|fleet_mgmt|Publisher|fleet/alerts/weather/alert1|fleet/#|
|vehicle1|vehicles|Subscriber|fleet/alerts/#|fleet/#|
|vehicle2|vehicles|Subscriber|fleet/alerts/#|fleet/#|


