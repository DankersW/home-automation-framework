from typing import Callable, Union
from json import dumps

from paho.mqtt import client as paho_mqtt

from home_automation_framework.logging.logging import Logging


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

    def connect(self) -> bool:
        self._mqtt_client = paho_mqtt.Client()
        try:
            self._mqtt_client.connect(host=self._config.get("broker"), port=self._config.get("port", None),
                                      keepalive=self._config.get("stay_alive", None))
            self._mqtt_client.on_connect = self._on_connect
            self._mqtt_client.on_message = self._on_message
            self._mqtt_client.loop_start()
        except (ConnectionRefusedError, TimeoutError) as err:
            self.log.error(f'Failed to connect to MQTT broker ({self._config.get("broker", None)}). Error: {err}')
            return False
        return True

    def _on_connect(self, _client, _userdata, _flags, _rc) -> None:
        self.log.success(f'Connected to MQTT broker ({self._config.get("broker")})')
        self._on_connect_callback()

    def _on_message(self, _client, _userdata, message) -> None:
        self.log.debug(f'Received message on topic {message.topic!r}')
        topic = message.topic
        payload = message.payload.decode("utf-8")
        self._on_message_callback(topic=topic, payload=payload)

    def publish(self, topic: str, msg: Union[dict, str]) -> bool:
        self.log.debug(f'Publishing message {msg!r} on topic {topic!r}')
        message_info = self._mqtt_client.publish(topic=topic, payload=dumps(msg), qos=1)
        if message_info.rc != 0:
            self.log.warning('Message did not get published successfully')
            return False
        return True

    def subscribe(self, topics: list) -> None:
        for topic in topics:
            self._mqtt_client.subscribe(topic=topic, qos=1)
