#!/usr/bin/env python3
from dataclasses import dataclass

import threading
import paho.mqtt.client as mqtt

from src.logging.logging import Logging, LogLevels
from src.lib.configuration_parser import ConfigurationParser


class LocalMqttGateway(threading.Thread):

    @dataclass
    class MqttConfiguration:
        port: int = 1883
        stay_alive: int = 60

    received_message_queue = []

    def __init__(self):
        threading.Thread.__init__(self)
        self.config = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)

        broker_address = self.config['local_mqtt_gateway']['broker_address']
        self.client = mqtt.Client()
        self.client.connect(broker_address, self.MqttConfiguration.port, self.MqttConfiguration.stay_alive)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def __del__(self):
        self.client.disconnect()

    def run(self):
        self.client.loop_forever()

    def on_connect(self, _client, _userdata, _flags, rc):
        self.log.success(f'Connected to MQTT broker with result code {str(rc)}.')
        self.client.subscribe("iot/#")

    def on_message(self, _client, _userdata, msg):
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        self.log.info(f'Received message {payload!r} on topic {topic!r}.')
        device_id = get_item_from_topic(topic, 'device_id')
        event = get_item_from_topic(topic, 'event')
        valid_topic = device_id is not None and payload is not None and event is not None
        if valid_topic:
            message = [device_id, payload, event]
            self.received_message_queue.append(message)
        else:
            pass
            # todo: print invalid dev_id or payload

    def get_last_message(self):
        message_queue = None
        if len(self.received_message_queue) > 0:
            message_queue = self.received_message_queue.pop(0)
        return message_queue

    def publish_control_message(self, device, data):
        topic = f'iot/{device}/control'
        self.log.info(f'Publishing message {data!r} on topic {topic!r}.')
        self.client.publish(topic, data)


def get_item_from_topic(topic, index_type):
    item_index = {
        'device_id': 1,
        'event': 2,
    }.get(index_type, None)
    dir_tree = topic.split('/')
    if len(dir_tree) != 3 or dir_tree[0] != "iot" or item_index is None:
        return None
    return dir_tree[item_index]


if __name__ == '__main__':
    mqtt_gateway = LocalMqttGateway()
