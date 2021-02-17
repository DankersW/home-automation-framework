from queue import Queue
from threading import Thread, Event
from datetime import datetime
from typing import Callable

from home_automation_framework.iot_gateway.mqtt_client import MqttClient
from home_automation_framework.iot_gateway.iot_message import IotMessage
from home_automation_framework.logging.logging import Logging
from home_automation_framework.utils.configuration_parser import ConfigurationParser


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
            # todo: unscribcribe from subject
            print("unsubcribe itself")

    def __del__(self):
        self.running = False

    def run(self):
        self._thread_ready.set()
        while self.running:
            queue_item = self._observer_notify_queue.get()
            print(queue_item)

    def notify(self, msg, _event):
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

        message = IotMessage(mqtt_topic=topic, data=payload)
        if message.is_valid():
            handler = self._select_handler(event=message.event)
            handler(msg=message)
        else:
            self.log.warning('The MQTT message is not valid')

    def _log_mqtt_traffic(self, topic: str, payload: str) -> None:
        msg = {'timestamp': datetime.now(), 'source': type(self).__name__, 'topic': topic, 'payload': payload}
        traffic_item = {'event': 'iot_traffic', 'message': msg}
        self._observer_publish_queue.put(traffic_item)

    def _select_handler(self, event: str) -> Callable:
        handler_map = {
            'state': self._handle_state_change,
            'telemetry': self._handle_telemetry
        }
        return handler_map.get(event, self._unknown_event)

    def _unknown_event(self, msg: IotMessage) -> None:
        self.log.warning(f'Unknown event {msg.event} - No action selected')

    def _handle_state_change(self, msg: IotMessage) -> None:
        self.log.debug("Handling state event")
        message = {'device_id': msg.device_id, 'event_type': msg.event, 'state': msg.payload.get('state')}
        item = {'event': 'device_state_changed', 'message': message}
        self._observer_publish_queue.put(item)

    def _handle_telemetry(self, msg: IotMessage) -> None:
        pass
