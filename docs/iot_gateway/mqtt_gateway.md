# MQTT gateway
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

  **Possible events**
  
| event_type             | Info                                                                  | 
|------------------------|-----------------------------------------------------------------------|
| iot_dev_state_change   | Device state got changed                                              | 
| iot_sensor_data_info   | Device sends sensor data                                              | 
