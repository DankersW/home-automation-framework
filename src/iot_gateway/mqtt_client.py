from typing import Callable
from time import sleep
from json import dumps

from paho.mqtt import client as paho_mqtt, MQTTException

from src.logging.logging import Logging


class IllegalArgumentError(ValueError):
    pass


class MqttClient:
    """ Basic wrapper around Paho mqtt """
    _mqtt_client = None

    def __init__(self, config: dict, connect_callback: Callable, message_callback: Callable) -> None:
        if self.valid_arguments(config=config, callbacks=[connect_callback, message_callback]):
            self._config = config
            self._on_connect_callback = connect_callback
            self._on_message_callback = message_callback
        self.log = Logging(owner=__file__, config=True)

    def __del__(self) -> None:
        pass

    @staticmethod
    def valid_arguments(config: dict, callbacks: list) -> bool:
        callables = [callable(callback) for callback in callbacks]
        valid = 'broker' in config and any(callables)
        if valid:
            return True
        raise IllegalArgumentError

    def connect(self) -> paho_mqtt:
        self._mqtt_client = paho_mqtt.Client()
        try:
            self._mqtt_client.connect(host=self._config.get("broker"), port=self._config.get("port", None),
                                      keepalive=self._config.get("stay_alive", None))
            self._mqtt_client.on_connect = self._on_connect_callback
            self._mqtt_client.on_message = self._on_message_callback
            self._mqtt_client.loop_start()
        except (ConnectionRefusedError, TimeoutError) as err:
            self.log.error(f'Failed to connect to MQTT broker ({self._config.get("broker", None)}). Error: {err}')
            return None
        self.log.success(f'Connected to MQTT broker ({self._config.get("broker")})')
        return self._mqtt_client

    def publish(self, topic: str, msg: dict) -> bool:
        self.log.debug(f'Publishing message ')
        json_payload = dumps(msg)
        resp = self._mqtt_client.publish(topic=topic, payload=json_payload, qos=1)
        print(resp)
        pass

# todo: work on publish message with tests
# todo: on message handler


def on_connect(_client, _userdata, _flags, rc):
    print("connect")


def on_message():
    print("message")


if __name__ == '__main__':
    test_config = {'broker': '127.0.0.1', 'port': 1883, 'stay_alive': 60}
    mqtt_client = MqttClient(config=test_config, connect_callback=on_connect, message_callback=on_message)
    print(mqtt_client.connect())
    sleep(4)
    msg = {'a': 123, 'b': 'test'}
    mqtt_client.publish(topic="test/hello", msg=msg)


