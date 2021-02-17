# MQTT gateway

 **All topics**
| Topic                             | Event type    | Info                                         |   |   |
|-----------------------------------|---------------|----------------------------------------------|---|---|
| iot/devices/<device-id>/command   | Command       | Used for changing the State of the device    |   |   |
| iot/devices/<device-id>/config    | Configuration | Used for changing the settings of the device |   |   |
| iot/devices/<device-id>/telemetry | Telemetry     | Used by the device to send streaming data (sensor)    |   |   |
| iot/devices/<device-id>/state     | State         | Used by the device to upload state changes   |   |   |

## Message payload
Message payload can be in JSON format or in binary
```json
{
  "state": true
}
```

### Example
`state`
- **topic**: iot/devices/device_test_001/state
- **payload**: {"state": true}

`telemetry`
- **topic**: iot/devices/device_test_001/telemetry
- **payload**: {"temperature": 21.05, "humidity": 25.03}


