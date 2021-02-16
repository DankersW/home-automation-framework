# Todo

## General
-  [ ] Handle closing down correctly

## Framework
-  [ ] If an observer failed to start up, it needs to be removed from the observer list
-  [ ] GBridge: re-write to use mqtt client
-  [ ] In docker compose map volume that holds temp to a docker volume; /sys/class/thermal/thermal_zone2/temp:/thermal/thermal_zone2/temp

## IOT-gateway
-  [ ] Integration tests of home automation, mocking input and checking the output 
-  [ ] Publish status of framework over mqtt 
-  [ ] Parsing sensor data message to internal message object

## Docker
-  [ ] MongoDB for production needs to point to a specific location on the host

## CI
-  [ ] Test MongoDB handler and mongo_db wrapper
-  [ ] integration test for MongoDB and Mosquitto
-  [ ] Full on system test feeding MQTT packages into the framework and comparing the db afterwards
-  [ ] Show code-coverage in readme via a badge
