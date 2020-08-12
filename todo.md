# Todo

## Documentation
- [ ] Update readme with recent info
- [ ] Update architectural overview

## Bugs
- [ ] g-bridge: Out of memory causes reconnection. and and up with connection code 4 - The client is not currently 
connected. then disconnect 5 - the connection was refused. This keeps going forever. connect --> disconnect --> ... 
1:40 hours to disconnect
- [ ] cloud function: light status not set in Firestore anylonger when the device state changes
- [ ] iot-gateway: upon receiving of the command topic it ('{"state": 1}') the state is not updated on the device.

## Logging
- [ ] Create a logging class that logs comparable to the logging module
- [ ] Have a ylm file that specifies the logging configuration: E.Q format, log to file or terminal, etc. 
- [ ] Unit tests for logging

## Cloud
- [x] GCP commands to create firebase
- [x] Include all cloud functions into 1 main and have each cloud function organized in one .py file
- [x] Cloud function that is triggered on attach/detach and sets the status online status of that device in firebase
- [ ] Get Google Asistent to talk to firebase, dialog flow, homegraph, actions, etc...
- [x] If data in firebase changes, write down to that client

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

## Embedded
- [x] If a devices boots up send a message to attach and if it is going down a detach message
- [ ] Get battery status of device
- [ ] On low battery call a disconnect function
- [ ] On low battery send out email to recharge 

## CI
- [x] Implement Actions on Github that runs a job to test if all tests pass before a merge to master or push to master
