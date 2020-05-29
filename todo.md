# Todo

## Cloud
- [ ] GCP commands to create firebase
- [x] Include all cloud functions into 1 main and have each cloud function orginized in one .py file
- [ ] Cloud function that is triggered on attach/detach and sets the status online status of that device in firebase


## Gateway
- [x] Re-write G-bridge to serve as a gateway instead of mocking each device
- [ ] Attach and detach devices when they turn on or off

## Full chain
- [ ] Fix crash when the cloud controls a device and device updates its status back
- [ ] Disconnecting of a device on all places + firebase state onile

## Embedded
- [ ] If a devices boots up send a message to attach and if it is going down a detach message