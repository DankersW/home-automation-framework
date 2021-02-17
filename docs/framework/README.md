# Framework

## IoT-observer messages
The core of the iot-gateway is based on the Observer pattern which has a Subject (the one who handles all the 
connections from the observers), a ConcreteSubject (which one decides when and what event needs to be delivered), and 
a bunch of observers which subscribe to certain events. 

| Event name             | Info                                                                     | Event generator(s) | Interested observers              |
|------------------------|--------------------------------------------------------------------------|--------------------|-----------------------------------|
| gcp\_state\_changed    | Describes that the state on GCP has changed, message arrives at G-bridge | G-bridge           | DB\_handler, local\_mqtt\_gateway |
| device\_state\_changed | Notifies that the state of any IoT device has been updated               | local-mqtt         | DB\_handler, G-bridge             |
| host\_health           | Publishes information about the state server's host machine              | host-monitor       | DB\_handler                       |
| iot\_traffic           | Used to publish the iot traffic to the DB\_handler for logging           | local-mqtt         | DB\_handler                       |
