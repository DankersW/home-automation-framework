from dataclasses import dataclass
from queue import Queue
from threading import Thread, Event
from json import loads
from datetime import datetime

from src.iot_gateway.mqtt_client import MqttClient

from src.logging.logging import Logging
from lib.configuration_parser import ConfigurationParser
from lib.utils import is_json


@dataclass
class MqttConfiguration:
    port: int = 1883
    stay_alive: int = 60


class MqttGateway(Thread):
    running = False
    subscribed_event = ['gcp_state_changed']

    def __init__(self, queue, thread_event: Event):
        Thread.__init__(self)
        self.config: dict = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)

        self._observer_notify_queue: Queue = Queue(maxsize=100)
        self._observer_publish_queue: Queue = queue
        self._thread_ready: Event = thread_event

        config = self.get_mqtt_config()
        self.mqtt_client = MqttClient(config=config, connect_callback=self.on_connect, message_callback=self.on_message)
        if not self.mqtt_client.connect():
            print("unsubcribe itself")

    def __del__(self):
        self.running = False

    def run(self):
        self._thread_ready.set()
        while self.running:
            queue_item = self._observer_notify_queue.get()
            print(queue_item)

    def notify(self, msg, _):
        self._observer_notify_queue.put(item=msg)

    def get_mqtt_config(self) -> dict:
        return {'broker': self.config['mqtt_gateway']['broker_address'], 'port': 1883, 'stay_alive': 60}

    def on_connect(self):
        topics = ['iot/#']
        self.mqtt_client.subscribe(topics=topics)
        self._thread_ready.set()
        self.running = True

    def on_message(self, topic: str, payload: str) -> None:
        self.log.info(f'Received {payload!r} on topic {topic!r}')
        self._log_mqtt_traffic(topic=topic, payload=payload)

        data = self._parse_mqtt_payload(payload=payload)
        if self._is_valid_mqtt_message(msg=data):
            self._message_handler(data=data)
        else:
            self.log.warning('The MQTT message is was not valid')

    def _log_mqtt_traffic(self, topic: str, payload: str) -> None:
        msg = {'timestamp': datetime.now(), 'source': type(self).__name__, 'topic': topic, 'payload': payload}
        traffic_item = {'event': 'iot_traffic', 'message': msg}
        self._observer_publish_queue.put(traffic_item)

    def _parse_mqtt_payload(self, payload: str) -> dict:
        if not is_json(payload):
            self.log.warning('Received message was not in JSON format.')
            return dict()
        return loads(payload)

    @staticmethod
    def _is_valid_mqtt_message(msg: dict) -> bool:
        needed_keys = ['device_id', 'event_type']
        for key in needed_keys:
            if key not in msg:
                return False
        return True

    def _message_handler(self, data: dict) -> None:
        action_map = {
            'iot_dev_state_change': self._handle_state_change
        }
        event = data.get('event_type')
        action = action_map.get(event, self._unknown_event)
        action(data)

    def _unknown_event(self, data: dict):
        self.log.warning(f'Unknown event {data.get("event_type")} - No action selected')

    def _handle_state_change(self, data: dict):
        pass

# todo: finish message handler
# todo: inplement handle_state_changee


if __name__ == '__main__':
    t_queue = Queue(10)
    t_event = Event()
    mqtt_gateway = MqttGateway(queue=t_queue, thread_event=t_event)
