from dataclasses import dataclass
from queue import Queue
from threading import Thread, Event

from src.logging.logging import Logging
from lib.configuration_parser import ConfigurationParser


@dataclass
class MqttConfiguration:
    port: int = 1883
    stay_alive: int = 60


class LocalMqttGateway(Thread):
    running = False
    subscribed_event = ['gcp_state_changed']

    def __init__(self, queue, thread_event: Event):
        Thread.__init__(self)
        self.config = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)

        self.observer_notify_queue = Queue(maxsize=100)
        self.observer_publish_queue = queue
        self._thread_ready = thread_event

        self.running = True

    def __del__(self):
        self.running = False

    def run(self):
        self._thread_ready.set()
        while self.running:
            queue_item = self.observer_notify_queue.get()

    def notify(self, msg, _):
        self.observer_notify_queue.put(item=msg)


if __name__ == '__main__':
    t_queue = Queue(10)
    t_event = Event()
    mqtt_gateway = LocalMqttGateway(queue=t_queue, thread_event=t_event)
