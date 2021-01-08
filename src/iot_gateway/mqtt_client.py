from typing import Callable
from time import sleep

from paho.mqtt import client as paho_mqtt, MQTTException

from src.logging.logging import Logging


class MqttClient:
    """ Basic wrapper around Paho mqtt """

    def __init__(self, config: dict, connect_callback: Callable, message_callback: Callable):
        self._config = config
        self._on_connect_callback = connect_callback
        self._on_message_callback = message_callback
        self.log = Logging(owner=__file__, config=True)

    def __del__(self):
        pass

    def connect(self) -> paho_mqtt:
        client = paho_mqtt.Client()
        try:
            client.connect(host=self._config.get("broker", None), port=self._config.get("port", None),
                           keepalive=self._config.get("stay_alive", None))
            client.on_connect = self._on_connect_callback
            client.on_message = self._on_message_callback
            client.loop_start()
        except (ConnectionRefusedError, TimeoutError) as err:
            self.log.error(f'Failed to connect to MQTT broker ({self._config.get("broker", None)}). Error: {err}')
            return None
        return client

    def publish(self):
        pass

    def ll(self, _client, _userdata, _flags, rc):
        print("mock connect")


def on_connect(_client, _userdata, _flags, rc):
    print("connect")


def on_message():
    print("message")


if __name__ == '__main__':
    test_config = {'broker': '127.0.0.1', 'port': 1883, 'stay_alive': 60}
    mqtt_client = MqttClient(config=test_config, connect_callback=on_connect, message_callback=on_message)
    print(mqtt_client.connect())
    sleep(5)
    mqtt_client.publish()

