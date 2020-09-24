# Todo

## General
- [x] Clean-up repo and create new repo's depending on the 'product'.
- [ ] Handle file path's correctly, maybe using a path translator file or the __init__.py

## Documentation
- [ ] Update readme with recent info
- [ ] Update architectural overview

## Bugs
- [ ] g-bridge: Out of memory causes reconnection. and and up with connection code 4 - The client is not currently 
connected. then disconnect 5 - the connection was refused. This keeps going forever. connect --> disconnect --> ... 
1:40 hours to disconnect
- [x] cloud function: light status not set in Firestore anylonger when the device state changes
- [x] iot-gateway: upon receiving of the command topic it ('{"state": 1}') the state is not updated on the device.
- [ ] Device gets detached from the GCP cloud when the state get's published to quickly (assuming) | error log: 
2020-07-16 10:14:28.182922 - GCP_GATEWAY | Received message '{"error_type":"GATEWAY_DETACHMENT_DEVICE_ERROR","description":"Device detached because of a device error.","device_id":"light_switch_001"}' on topic '/devices/home_automation_light_switches_gateway/errors'.
2020-07-16 10:14:49.227127 - GCP_GATEWAY | Received message '{"error_type":"GATEWAY_DEVICE_NOT_FOUND","description":"The specified device with ID 'light_switch_001' is not attached to the gateway.","device_id":"light_switch_001","mqtt_message_info":{"message_type":"PUBLISH","topic":"/devices/light_switch_001/state","packet_id":10}}' on topic '/devices/home_automation_light_switches_gateway/errors'.
Device needs to be reconnected when this error is handled. 
- [ ] Fix folder structure

## Logging
- [x] Create a logging class that logs comparable to the logging module
- [x] Have a ylm file that specifies the logging configuration: E.Q format, log to file or terminal, etc. 
- [x] Unit tests for logging
- [ ] Usage YML file to set configuration
- [ ] Set file name to date, and have all write to the same one
- [ ] Set logging name via __repr__ or __name__ | or # Create a logger with the same name as this file logger = logging.getLogger(Path(__file__).name)
- [ ] Switch to f string printing

## Testing
- [ ] Test environment for running development tests

## Gateway
- [x] Re-write G-bridge to serve as a gateway instead of mocking each device
- [x] Attach and detach devices when they turn on or off
- [x] Reattach all connected devices when the gateway disconnects
- [ ] Sending data: include a time-off that the functions waits for a ACK. after the timeout either drop the message or resend it  
- [x] Fix path issue

## Full chain
- [x] Fix crash when the cloud controls a device and device updates its status back
- [ ] Disconnecting of a device on all places + firebase state online
- [ ] Map device id to physical placement in the apartment 
- [ ] Let a device generate it's own random ID when it boots up for the first time, check a local file if this ID is already used or not.

## CI
- [x] Implement Actions on Github that runs a job to test if all tests pass before a merge to master or push to master
- [x] Update tests to look for updated path to tests. and include all new tests
- [x] Static code analyisis with Lint
- [x] Code test coverage
- [ ] Create a first release

## Enviroment
- [ ] Setup a virtual environment
- [ ] Docker-ize environment
