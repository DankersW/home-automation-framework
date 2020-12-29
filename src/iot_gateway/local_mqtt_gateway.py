from dataclasses import dataclass
from queue import Queue
from json import loads
from datetime import datetime

from threading import Thread, Event

from paho.mqtt import client as mqtt

from src.logging.logging import Logging
from lib.configuration_parser import ConfigurationParser


class LocalMqttGateway(Thread):

    @dataclass
    class MqttConfiguration:
        port: int = 1883
        stay_alive: int = 60

    running = False
    subscribed_event = ['gcp_state_changed']

    def __init__(self, queue, thread_event: Event):
        Thread.__init__(self)
        self.config = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)

        self.observer_notify_queue = Queue(maxsize=100)
        self.observer_publish_queue = queue
        self._thread_ready = thread_event

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
        self._thread_ready.set()
        while self.running:
            queue_item = self.observer_notify_queue.get()
            self.publish(msg=queue_item)

    def notify(self, msg, _):
        self.observer_notify_queue.put(item=msg)

    def on_connect(self, _client, _userdata, _flags, rc):
        self.log.success(f'Connected to MQTT broker with result code {str(rc)}.')
        self.client.subscribe("iot/#")

    def on_message(self, _client, _userdata, msg):
        data = loads(msg.payload.decode('utf-8'))
        topic = msg.topic
        device_id = data.get('device_id', None)
        event = data.get('event_type', None)
        self.log.info(f'Received message {data!r} on topic {topic!r}.')

        bad_msg = device_id is None or event is None
        if bad_msg:
            self.log.warning(f'Invalid message received on topic {event!r} with device_id {device_id!r}')
        elif event == 'iot_dev_state_change':
            device_state = data.get('state', None)
            item = {'event': 'device_state_changed',
                    'message': {'device_id': device_id, 'event_type': event, 'state': device_state}}
            self.observer_publish_queue.put(item)

        self._save_iot_message(topic=topic, payload=data)

    def publish(self, msg):
        topic = None
        device = msg.get('device_id')
        if msg.get('event_type') == 'command':
            topic = f'iot/devices/{device}/command'

        data = msg.get('payload', None)
        if topic is not None and data is not None:
            self.log.info(f'Publishing message {data!r} on topic {topic!r}.')
            self.client.publish(topic, data)

    def _save_iot_message(self, topic: str, payload: dict) -> None:
        traffic_item = {'event': 'iot_traffic', 'message': {'timestamp': datetime.now(),
                                                            'source': type(self).__name__,
                                                            'topic': topic, 'payload': payload}}
        self.observer_publish_queue.put(traffic_item)


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
    t_event = Event()
    mqtt_gateway = LocalMqttGateway(queue=t_queue, thread_event=t_event)
