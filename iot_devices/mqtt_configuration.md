# MQTT Configuration
This document specifies how MQTT between our IoT deviced and the on-site server is setup. These devices are at the 
using a not-sercured version of MQTT because of the security overhead on the IoT devices as well as these devices are 
not directly connected to the internet. 

|               | Info          |
| ------------- |:-------------:|
| MQTT broker   | Mosquitto     |
| MQTT address  | 192.168.1.125 |
| MQTT port     | 1883          |


Each device has its own device id e.q. (device-001). There exist 3 topics, one subscription, one publish, and one
general topic. 
The general structure of the topics follows the pattern:
```
iot/device_id/topic
```

## Topics

### Wildcard topic
Used <b> only </b> by the device gateway running on the home server. In this way the server can subscribe to all the connected 
devices at once. It distinguishes between which device has sends what by using the device ID
```
iot/#
```

### Control topic
Used by device gateway to send control messages to a particular device. These control messages could be for example; 
set the light state to True. Every device listens to this topic (one topic per device) for things to do.
```
iot/device-001/control
```

### State topic
Used by a device to publish information to the device gateway. Each device publishes state information on this topic. 
For example; the state of the light switch has changed via input by the user. The device will now publish this change 
on the state topic so that the device gateway knows of the change.
```
iot/device-001/state
```

### Attach topic
Used by the iot device to notify the gateway that it has come alive. 
The content of the message is empty
```
iot/device-001/attach
```

### Configuration topic
<b>TBD</b>



## Message content
To keep the messages as short as possible, the content will consists of only one single binary number. For example if 
the user changes the state of the light switch from OFF to ON which is connected to device 001. Then device 001 will publish to the 
following topic with payload of 1
```
iot/device-001/state --> payload "1"
```