#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime


# used for ...
class DeviceGateway:
    MQTT_BROKER_ADDRESS = "10.42.0.25"#"192.168.1.125"
    MQTT_PORT = 1883
    MQTT_STAYALIVE = 60

    last_data = ""

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(self.MQTT_BROKER_ADDRESS, self.MQTT_PORT, self.MQTT_STAYALIVE)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_forever()

    def __del__(self):
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe("iot/#")

    def on_message(self, client, userdata, msg):
        time = datetime.datetime.now()
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        print("{} | Topic: \"{}\" \t Message: \"{}\"".format(time, topic, payload))
        self.last_data = payload