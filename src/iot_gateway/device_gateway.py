#!/usr/bin/env python3

from src.logging.logging import Logging, LogLevels


import threading
import paho.mqtt.client as mqtt



class DeviceGateway(threading.Thread):
    MQTT_BROKER_ADDRESS = "192.168.1.125"#"10.42.0.25"
    MQTT_PORT = 1883
    MQTT_STAYALIVE = 60

    received_message_queue = []

    def __init__(self):
        threading.Thread.__init__(self)
        self.log = Logging(owner='IoT device gateway', log_mode='terminal', min_log_lvl=LogLevels.debug)
        self.client = mqtt.Client()
        self.client.connect(self.MQTT_BROKER_ADDRESS, self.MQTT_PORT, self.MQTT_STAYALIVE)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def __del__(self):
        self.client.disconnect()

    def run(self):
        self.client.loop_forever()

    def on_connect(self, _client, _userdata, _flags, rc):
        self.log.success('Connected to MQTT broker with result code {}.'.format(str(rc)))
        self.client.subscribe("iot/#")

    def on_message(self, _client, _userdata, msg):
        payload = msg.payload.decode('utf-8')
        topic = msg.topic
        self.log.info('Received message \'{}\' on topic \'{}\'.'.format(payload, topic))
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
        topic = "iot/{}/control".format(device)
        self.log.info('Publishing message \'{}\' on topic \'{}\'.'.format(data, topic))
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
    device_gateway = DeviceGateway()
