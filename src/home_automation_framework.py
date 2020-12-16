from time import sleep
from queue import Queue

from lib.configuration_parser import ConfigurationParser
from src.logging.logging import Logging
from src.iot_gateway.g_bridge import GBridge
from src.iot_gateway.local_mqtt_gateway import LocalMqttGateway
from src.db.db_handler import DbHandler


class Subject:
    def __init__(self, events) -> None:
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event) -> dict:
        return self.events[event]

    def register(self, events, obs_object, callback=None) -> None:
        if callback is None:
            callback = getattr(obs_object, 'notify')
        for event in events:
            self.get_subscribers(event)[obs_object] = callback

    def unregister(self, event, obs_object) -> None:
        del self.get_subscribers(event)[obs_object]

    def dispatch(self, event, message) -> None:
        for _, callback in self.get_subscribers(event).items():
            callback(message, event)


class IotSubject:
    observers = []
    running = False

    def __init__(self) -> None:
        events = ['gcp_state_changed', 'device_state_changed', 'iot_traffic']
        self.log = Logging(owner=__file__, config=True)
        self.config = ConfigurationParser().get_config()
        self.subject = Subject(events)

        self.observer_queue = Queue(maxsize=100)

        self.init_observers()
        self.attach_observers()
        self.start_observer_threats()

    def init_observers(self) -> None:
        if self.config['system_components']['gcp']:
            self.observers.append({'obs_object': GBridge(queue=self.observer_queue),
                                   'events': ['device_state_changed']})

        if self.config['system_components']['local_mqtt_gateway']:
            self.observers.append({'obs_object': LocalMqttGateway(queue=self.observer_queue),
                                   'events': ['gcp_state_changed']})

        if self.config['system_components']['db']:
            self.observers.append({'obs_object': DbHandler(queue=self.observer_queue),
                                   'events': ['gcp_state_changed', 'device_state_changed', 'iot_traffic']})

    def attach_observers(self) -> None:
        for observer in self.observers:
            self.subject.register(**observer)

    def start_observer_threats(self) -> None:
        for observer in self.observers:
            observer.get('obs_object').start()
        observer_names = [key['obs_object'] for key in self.observers]
        self.log.success(f'Started {len(observer_names)} observers. {observer_names}')
        sleep(5)  # To make sure every component has started up correctly
        self.running = True

    def run(self):
        while self.running:
            event = self.get_observer_events()
            self.notify_observers(event=event)

    def notify_observers(self, event):
        self.subject.dispatch(**event)

    def get_observer_events(self) -> dict:
        return self.observer_queue.get()


if __name__ == '__main__':
    iot_subject = IotSubject()
    iot_subject.run()
