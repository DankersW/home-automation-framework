from typing import Callable

from paho.mqtt import client as paho_mqtt, MQTTException


class MqttHandler:
    """ Basic wrapper around Paho mqtt """

    def __init__(self, config: dict, connect_callback: Callable, message_callback: Callable):
        self._on_connect_callback = connect_callback
        self._on_message_callback = message_callback

    def __del__(self):
        pass

    def _connect_mqtt_client(self, broker_address: str, port: int, stay_alive: int) -> paho_mqtt:
        client = paho_mqtt.Client()
        try:
            client.connect(host=broker_address, port=port, keepalive=stay_alive)
            client.on_connect = self._on_connect_callback
            client.on_message = self._on_message_callback
            client.loop_start()
        except (ConnectionRefusedError, TimeoutError) as err:
            self._failed_connection(msg=err.strerror)
        return client

    def publish(self):
        pass