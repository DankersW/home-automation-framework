# Todo

## General
-  [ ] Handle closing down correctly

## Framework
-  [ ] If an observer failed to start up, it needs to be removed from the observer list
-  [ ] GBridge: re-write to use mqtt client

## IOT-gateway
-  [ ] Integration tests of home automation, mocking input and checking the output 

## Environment
-  [ ] virtual enviroment that adds paths to PYTHONPATH
-  [ ] run.sh script that set's up the entire project as well as the virtual env

## Docker
-  [ ] MongoDB for production needs to point to a specific location on the host
-  [ ] Docker image holding the application

## CI
-  [ ] Create a first release to docker hun
-  [ ] Test MongoDB handler and mongo_db wrapper
-  [ ] integration test for MongoDB and Mosquitto
-  [ ] Full on system test feeding MQTT packages into the framework and comparing the db afterwards
-  [ ] Show code-coverage in readme via a badge
