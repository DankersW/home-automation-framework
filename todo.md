# Todo

## Needed
- [ ] Bumb test coverage
- [ ] Rewrite mongo and db_handler in a proper way

## Features
-  [ ] Better logging info, debug showing which event is handeling what data.
-  [ ] Testing: Create Integration tests (without mongo and mqtt docker) and System tests (with sandbox docker compose) in a sandbox
-  [ ] Update documentation
-  [ ] Re-think the DB, useing device_objectId in other documents instead of a raw name
-  [ ] Closing down correctly

## Bugs 
-  [ ] If an observer failed to start up, it needs to be removed from the observer list
-  [ ] Writing to DB locally and from docker the time is different, locally correct time, via docker -2 hours timestamp
-  [ ] Fix handing threaths when killing the system