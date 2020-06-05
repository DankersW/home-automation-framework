# Todo

## Cloud
- [ ] GCP commands to create firebase
- [x] Include all cloud functions into 1 main and have each cloud function organized in one .py file
- [ ] Cloud function that is triggered on attach/detach and sets the status online status of that device in firebase
- [ ] Get Google Asistent to work

## Gateway
- [x] Re-write G-bridge to serve as a gateway instead of mocking each device
- [x] Attach and detach devices when they turn on or off
- [x] Reattach all connected devices when the gateway disconnects
- [ ] Sending data: include a time-off that the functions waits for a ACK. after the timeout either drop the message or resend it  

## Full chain
- [x] Fix crash when the cloud controls a device and device updates its status back
- [ ] Disconnecting of a device on all places + firebase state online
- [ ] Map device id to physical placement in the apartment 

## Embedded
- [x] If a devices boots up send a message to attach and if it is going down a detach message
- [ ] Get battery status of device
- [ ] On low battery call a disconnect function
- [ ] On low battery send out email to recharge 