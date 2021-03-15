# Todo

## General

## Framework
-  [ ] If an observer failed to start up, it needs to be removed from the observer list
-  [ ] GBridge: re-write to use mqtt client
-  [ ] Using an ObserverMessage object instead of a dict

## IOT-gateway
-  [ ] Integration tests of home automation, mocking input and checking the output 
-  [ ] Publish status of framework over mqtt 
-  [ ] MQTT client ping pong, so that we can validate that the framework is working correctly

## Docker
-  [ ] MongoDB for production needs to point to a specific location on the host

## CI
-  [ ] Test MongoDB handler and mongo_db wrapper
-  [ ] integration test for MongoDB and Mosquitto
-  [ ] Full on system test feeding MQTT packages into the framework and comparing the db afterwards
-  [ ] Integration tests
-  [ ] System tests
-  [ ] When a tag is created on github do a docker build and push for both architectures using buildx, the tag version equals to the git tag

### Prio
-  [ ] Run system test
-  [ ] FrameworkMessageObject
