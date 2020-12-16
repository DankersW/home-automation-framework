# Todo

## General
-  [x] Clean-up repo and create new repo's depending on the 'product'.
-  [x] Handle file path's correctly, maybe using a path translator file or the __init__.py
-  [x] Licensing
-  [x] Docs folder
-  [ ] Handle closing down correctly
-  [x] Fix include path for license file (G-bridge)
-  [x] Update linting script for github workflows
-  [x] Use proper threath queue and threath event between the observers and the subject. so that we don't need to do active polling
-  [x] G-bridge: message from new device --> attach that device first

## Documentation
-  [x] Update readme with recent info
-  [x] Update architectural overview

## IOT-gateway
-  [x] Find and implement a good pattern to run the message shuffeling based on active gateways
-  [x] Publish data from the notify to all observers
-  [x] Update the outgoing messages queue
-  [ ] Threating event to let all the threats wait to start untill all observers are set
-  [x] Attach devices automatically
-  [x] Document naming of the different events and clean it up in the code so that the deivces listen to them in a good way
-  [x] Define iot (mqtt) message content that is send from devices
-  [ ] Clean way of initialzing all observers instead of if a then x. e.q. fetching them a different file. 
-  [ ] Fetch observer interested messages from the class itself.

## Bugs
-  [ ] g-bridge: Out of memory causes reconnection. and and up with connection code 4 - The client is not currently 
connected. then disconnect 5 - the connection was refused. This keeps going forever. connect --> disconnect --> ... 1:40 hours to disconnect
-  [x] cloud function: light status not set in Firestore anylonger when the device state changes
-  [x] iot-gateway: upon receiving of the command topic it ('{"state": 1}') the state is not updated on the device.
-  [ ] Device gets detached from the GCP cloud when the state get's published to quickly (assuming) | error log: 
2020-07-16 10:14:28.182922 - GCP_GATEWAY | Received message '{"error_type":"GATEWAY_DETACHMENT_DEVICE_ERROR","description":"Device detached because of a device error.","device_id":"light_switch_001"}' on topic '/devices/home_automation_light_switches_gateway/errors'.
2020-07-16 10:14:49.227127 - GCP_GATEWAY | Received message '{"error_type":"GATEWAY_DEVICE_NOT_FOUND","description":"The specified device with ID 'light_switch_001' is not attached to the gateway.","device_id":"light_switch_001","mqtt_message_info":{"message_type":"PUBLISH","topic":"/devices/light_switch_001/state","packet_id":10}}' on topic '/devices/home_automation_light_switches_gateway/errors'.
Device needs to be reconnected when this error is handled. 
-  [x] Fix folder structure

## Logging
-  [x] Create a logging class that logs comparable to the logging module
-  [x] Have a ylm file that specifies the logging configuration: E.Q format, log to file or terminal, etc. 
-  [x] Unit tests for logging
-  [x] Usage YML file to set configuration
-  [x] Set file name to date, and have all write to the same one
-  [x] Set logging name via __repr__ or __name__ or __file__
-  [x] Switch to f string printing
-  [x] Log to DB aswell


## Storage
-  [x] DB that stores current state data (E.Q. Document DB like mongodb)
-  [x] DB that stores data for a long time (E.Q. wide column db like Apache Cassandra or Apache HBase)
-  [x] save state changes in one document
-  [x] Log all iot messages that goes back and forward

## GUI
-  [ ] Front-end to visualize db data
-  [ ] way to send data to iot-framework
-  [ ] Log iot-messages in the gui

## Testing
-  [ ] Verification environment for running development tests

## Gateway
-  [x] Re-write G-bridge to serve as a gateway instead of mocking each device
-  [x] Attach and detach devices when they turn on or off
-  [x] Reattach all connected devices when the gateway disconnects
-  [ ] Sending data: include a time-off that the functions waits for a ACK. after the timeout either drop the message or resend it  
-  [x] Fix path issue

## Full chain
-  [x] Fix crash when the cloud controls a device and device updates its status back

## CI
-  [x] Implement Actions on Github that runs a job to test if all tests pass before a merge to master or push to master
-  [x] Update tests to look for updated path to tests. and include all new tests
-  [x] Static code analyisis with Lint
-  [x] Code test coverage
-  [ ] Create a first release and install https://realpython.com/pyinstaller-python/

## Release
-  [ ] when monitoring and email notifications is in place
-  [ ] messaging gateway is running
-  [ ] db working 
-  [ ] proper logging
-  [ ] observer pattern

## Environment
-  [x] Setup ubuntu home-server with  MQTT broker and MongoDB db
-  [x] Run from same place always
-  [x] script to run linting and testing locally

## Docker
-  [ ] Container holding Mongo-db + mqtt

## Monitoring
-  [ ] Have a host-monitoring observer that publishes its data to the db handler with a good event name
-  [ ] Health checking - health tracing - message tracing

## Server
-  [ ] Log some HW perifials
-  [ ] Monitoring of the themperature and sending out reacting on to high temp, send out warning email if it get's warm
