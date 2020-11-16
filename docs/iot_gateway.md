# Docs

## Protocols
The Home Server has two MQTT instances, one that forwards messages from Device Gateway to the GCP IoT core and vice 
versa. And One that forwards messages from the IoT devices to and from the G-bridge.


## IoT-gateway message content
Data is passed along all the observers in a Dict format.

| Name       | Info                                          | Example      | Madatory | Data type                   |
|------------|-----------------------------------------------|--------------|----------|-----------------------------|
| device_id  | The id of the device the message belongs to   | 'device_abc' | Yes      | string                      |
| event_type | Type of event                                 | 'telemetry'  | Yes      | <telemerty, state, command> |
| payload    | Payload of the message, depends on event_type | true         | Yes      | <bool, int>                 |
| extra      | Extra data in the form of json                | {"abc": 123} | No       | JSON                        |

### G-bridge MQTT configuration
Google's IoT core MQTT broker has 4 predefined topics. 
* **Configuration:** Sent from the cloud to the device, up to one message per second. Configuration messages are guaranteed
 to be delivered to the device.
* **Commands:** Send up to 100 messages per second from the cloud to the device. Commands are only delivered if the device
 is online.
* **State:** Sent from the device to the cloud, up to one message per second. State updates are delivered to active Pub/Sub
 subscribers and recent updates are persisted inside Cloud IoT Core.
* **Telemetry:** Send up to 100 messages per second from the device to the cloud. Telemetry events are only delivered to
 active Pub/Sub subscribers.

![Google_Mqtt](../resources/images/google_mqtt.png "Google MQTT overview")

|               | Info                  |
| ------------- |:---------------------:|
| MQTT broker   | Cloud IoT core        |
| MQTT address  | mqtt.googleapis.com   |
| MQTT port     | 8883                  |
| Security      | RS256                 |

#### Topics
**Configuration**
```
/devices/{device-id}/config
```
**Commands**
```
/devices/{device-id}/commands
```
**State**
```
/devices/{device-id}/state
```
**Telemetry**
```
/devices/{device-id}/events
```

**Message content**
The messages contain a JSON string with explenatory key value pairs. For example, in the case of of a light switch 
updating its status to the cloud. It could send the following message on the topic 
``` /devices/lightswitch-001/state ```.
```
{"light_state": 1}
```
