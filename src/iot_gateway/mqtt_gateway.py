from dataclasses import dataclass
from queue import Queue
from threading import Thread, Event

from src.iot_gateway.mqtt_client import MqttClient

from src.logging.logging import Logging
from lib.configuration_parser import ConfigurationParser


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

        mqtt_config = self.get_mqtt_config()
        mqtt_client = MqttClient(config=mqtt_config, connect_callback=self.on_connect, message_callback=self.on_message)
        self.mqtt_client = mqtt_client.connect()

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

    def on_connect(self, _client, _userdata, _flags, _rc):
        self.log.success(f'Connected to MQTT broker ({self.config["mqtt_gateway"]["broker_address"]})')
        self._thread_ready.set()
        self.running = True

    def on_message(self):
        pass

    # todo: test mosquitto broker tests
    #  github https://github.com/marketplace/actions/mosquitto-mqtt-broker-in-github-actions
    # todo: integration tests local via docker, remote on github


if __name__ == '__main__':
    t_queue = Queue(10)
    t_event = Event()
    mqtt_gateway = MqttGateway(queue=t_queue, thread_event=t_event)
