# Todo

## Needed
- [ ] Re-think the DB, useing device_objectId in other documents instead of a raw name
- [ ] Bumb test coverage

## Features
-  [ ] MQTT ping-pong message from client to framework and back to client, usefull to validate that the framework is working
-  [ ] Better logging info, debug showing which event is handeling what data.
-  [ ] Testing: Create Integration tests (without mongo and mqtt docker) and System tests (with sandbox docker compose) in a sandbox
-  [ ] Publish status over MQTT
-  [ ] Update documentation

## Bugs 
-  [ ] If an observer failed to start up, it needs to be removed from the observer list
-  [ ] Writing to DB locally and from docker the time is different, locally correct time, via docker -2 hours timestamp