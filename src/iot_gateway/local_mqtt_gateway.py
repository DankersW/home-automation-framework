#!/usr/bin/env python3
from dataclasses import dataclass
from queue import Queue

import threading
import paho.mqtt.client as mqtt

from src.logging.logging import Logging
from lib.configuration_parser import ConfigurationParser


class LocalMqttGateway(threading.Thread):

    @dataclass
    class MqttConfiguration:
        port: int = 1883
        stay_alive: int = 60

    running = False

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.config = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)

        self.publish_queue = Queue(maxsize=100)
        self.received_queue = queue

        broker_address = self.config['local_mqtt_gateway']['broker_address']
        self.client = mqtt.Client()
        self.client.connect(broker_address, self.MqttConfiguration.port, self.MqttConfiguration.stay_alive)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.running = True

    def __del__(self):
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()

    def run(self):
        self.client.loop_start()
        while self.running:
            queue_item = self.publish_queue.get()
            self.publish(msg=queue_item)

    def notify(self, msg, _):
        self.publish_queue.put(item=msg)

    def on_connect(self, _client, _userdata, _flags, rc):
        self.log.success(f'Connected to MQTT broker with result code {str(rc)}.')
        self.client.subscribe("iot/#")

    def on_message(self, _client, _userdata, msg):
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        self.log.info(f'Received message {payload!r} on topic {topic!r}.')
        device_id = get_item_from_topic(topic, 'device_id')
        event = get_item_from_topic(topic, 'event')
        valid_topic = device_id is not None and payload is not None and event is not None and event != 'command'
        if valid_topic:
            queue_message = {'device_id': device_id, 'event_type': event, 'payload': payload}
            item = {'event': 'device_state_changed', 'message': queue_message}
            self.received_queue.put(item)
        else:
            pass
            # todo: print invalid dev_id or payload

    def publish(self, msg):
        topic = None
        device = msg.get('device_id')
        if msg.get('event_type') == 'command':
            topic = f'iot/devices/{device}/command'

        data = msg.get('payload', None)
        if topic is not None and data is not None:
            self.log.info(f'Publishing message {data!r} on topic {topic!r}.')
            self.client.publish(topic, data)


def get_item_from_topic(topic, index_type):
    item_index = {
        'device_id': 2,
        'event': 3,
    }.get(index_type, None)
    dir_tree = topic.split('/')
    if len(dir_tree) != 4 or dir_tree[0] != "iot" or item_index is None:
        return None
    return dir_tree[item_index]


if __name__ == '__main__':
    t_queue = Queue(10)
    mqtt_gateway = LocalMqttGateway(queue=t_queue)

