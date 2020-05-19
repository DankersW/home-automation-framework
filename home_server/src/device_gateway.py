#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import threading

INSTANCE_NAME = "Device-gateway"


class DeviceGateway(threading.Thread):
    MQTT_BROKER_ADDRESS = "10.42.0.25"#"192.168.1.125"
    MQTT_PORT = 1883
    MQTT_STAYALIVE = 60

    received_message_queue = []

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = mqtt.Client()
        self.client.connect(self.MQTT_BROKER_ADDRESS, self.MQTT_PORT, self.MQTT_STAYALIVE)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def __del__(self):
        self.client.disconnect()

    def run(self):
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        current_time = datetime.datetime.now()
        print("{} - {} | Connected to MQTT broker with result code {}".format(current_time, INSTANCE_NAME, str(rc)))
        self.client.subscribe("iot/#")

    def on_message(self, client, userdata, msg):
        current_time = datetime.datetime.now()
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        event = "state"
        print("{} - {} | Received message \'{}\' on topic \'{}\'.".format(current_time, INSTANCE_NAME, payload, topic))
        device_id = get_id_from_topic(topic)
        valid_topic = device_id is not None and payload is not None
        if valid_topic:
            message = [device_id, payload, event]
            self.received_message_queue.append(message)
        else:
            pass
            # todo: print invalid dev_id or payload

    def get_last_message(self):
        if len(self.received_message_queue) > 0:
            return self.received_message_queue.pop(0)
        else:
            return None

    def publish_control_message(self, device, data):
        topic = "iot/{}/control".format(device)
        current_time = datetime.datetime.now()
        print("{} - {} | Publishing message \'{}\' on topic \'{}\'.".format(current_time, INSTANCE_NAME, data, topic))
        self.client.publish(topic, data)


def get_id_from_topic(topic):
    index_device_id = 1
    dir_tree = topic.split('/')
    if len(dir_tree) != 3 or dir_tree[0] != "iot":
        return None
    return dir_tree[index_device_id]


if __name__ == '__main__':
    device_gateway = DeviceGateway()
