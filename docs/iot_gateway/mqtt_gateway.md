# MQTT gateway

 **All topics**

| Topic                             | Event type    | Info                                         |   |   |
|-----------------------------------|---------------|----------------------------------------------|---|---|
| iot/devices/<device-id>/command   | Command       | Used for changing the State of the device    |   |   |
| iot/devices/<device-id>/config    | Configuration | Used for changing the settings of the device |   |   |
| iot/devices/<device-id>/telemetry | Telemetry     | Used by the device to send streaming data (sensor)    |   |   |
| iot/devices/<device-id>/state     | State         | Used by the device to upload state changes   |   |   |
| iot/devices/<device-id>/system    | System        | Used by the system to poll and report for information about the system   |   |   |

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

`system` Device reporting
- **topic**: iot/devices/device_test_001/system
- **payload**: {"active": true}

`system` Framework requesting
- **topic**: iot/devices/framework/system
- **payload**: {"event": "poll info"}



