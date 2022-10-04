$BasePath = "/subscriptions/bdf55cdd-8dab-4cf4-9b2f-c21e8a780472/resourceGroups/slbojanic-rg/providers/Microsoft.EventGrid/namespaces/Scenario0"

armclient login dogfood

armclient PUT $BasePath?api-version=2022-10-15-preview resources\NS_Scenario0.json

armclient PUT $BasePath/caCertificates/test-ca-cert?api-version=2022-10-15-preview resources\CACertificate.json

armclient PUT $BasePath/topicSpaces/hello?api-version=2022-10-15-preview resources\TS_hello.json

armclient PUT $BasePath/clients/pub_client?api-version=2022-10-15-preview resources\C_pub_client.json

armclient PUT $BasePath/clients/sub_client?api-version=2022-10-15-preview resources\C_sub_client.json

armclient PUT $BasePath/clientGroups/all0?api-version=2022-10-15-preview resources\CG_all0.json

armclient PUT $BasePath/permissionBindings/sub-hello?api-version=2022-10-15-preview resources\PB_subscriber.json

armclient PUT $BasePath/permissionBindings/pub-hello?api-version=2022-10-15-preview resources\PB_publisher.json
