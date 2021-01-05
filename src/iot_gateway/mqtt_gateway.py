from dataclasses import dataclass
from queue import Queue
from threading import Thread, Event

from paho.mqtt import client as paho_mqtt, MQTTException

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

        self._mqtt_client = self._connect_mqtt_client(broker_address=self._get_broker_address())

    def __del__(self):
        self.running = False

    def run(self):
        self._thread_ready.set()
        while self.running:
            queue_item = self._observer_notify_queue.get()
            print(queue_item)

    def notify(self, msg, _):
        self._observer_notify_queue.put(item=msg)

    def _get_broker_address(self) -> str:
        return self.config['mqtt_gateway']['broker_address']

    def _connect_mqtt_client(self, broker_address: str) -> paho_mqtt:
        client = paho_mqtt.Client()
        try:
            client.connect(host=broker_address, port=1883, keepalive=60)
            client.on_connect = self._on_connect
            client.on_message = self._on_message
            client.loop_start()
        except (ConnectionRefusedError, TimeoutError) as err:
            self._failed_connection(msg=err.strerror)
        return client

    def _failed_connection(self, msg: str) -> None:
        mqtt_host = self.config['mqtt_gateway']['broker_address']
        self.log.error(f'Failed to connect to MQTT broker at address {mqtt_host} with error msg: {msg}')
        self._thread_ready.set()
        self.running = False
        # todo: unsubscribe mqtt from list

    def _on_connect(self, _client, _userdata, _flags, _rc):
        mqtt_host = self.config['mqtt_gateway']['broker_address']
        self.log.success(f'Connected to MQTT broker at address {mqtt_host}')
        self._thread_ready.set()
        self.running = True

    def _on_message(self):
        pass

    # todo: test mosquitto broker tests
    #  github https://github.com/marketplace/actions/mosquitto-mqtt-broker-in-github-actions
    # todo: integration tests local via docker, remote on github


if __name__ == '__main__':
    t_queue = Queue(10)
    t_event = Event()
    mqtt_gateway = MqttGateway(queue=t_queue, thread_event=t_event)
