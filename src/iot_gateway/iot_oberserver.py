from time import sleep

from lib.configuration_parser import ConfigurationParser
from src.logging.logging import Logging
from src.iot_gateway.g_bridge import GBridge
from src.iot_gateway.local_mqtt_gateway import LocalMqttGateway
from src.db.db_handler import DbHandler


class Subject:
    def __init__(self, events):
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, events, obs_object, callback=None):
        if callback is None:
            callback = getattr(obs_object, 'notify')
        for event in events:
            self.get_subscribers(event)[obs_object] = callback

    def unregister(self, event, obs_object):
        del self.get_subscribers(event)[obs_object]

    def dispatch(self, event, message):
        for _, callback in self.get_subscribers(event).items():
            callback(message, event)


class IotSubject:
    observers = []

    def __init__(self):
        events = ['gcp_mqtt', 'device_mqtt']
        self.log = Logging(owner=__file__, config=True)
        self.config = ConfigurationParser().get_config()
        self.subject = Subject(events)

        self.init_observers()
        self.attach_observers()
        self.start_observer_threats()

    def init_observers(self):
        if self.config['system_components']['gcp']:
            self.observers.append({'obs_object': GBridge(), 'events': ['gcp_mqtt']})

        if self.config['system_components']['local_mqtt_gateway']:
            self.observers.append({'obs_object': LocalMqttGateway(), 'events': ['device_mqtt']})

        if self.config['system_components']['db']:
            self.observers.append({'obs_object': DbHandler(), 'events': ['device_mqtt', 'gcp_mqtt']})

    def attach_observers(self):
        for observer in self.observers:
            self.subject.register(**observer)

    def start_observer_threats(self):
        for observer in self.observers:
            observer.get('obs_object').start()
        observer_names = [key['obs_object'] for key in self.observers]
        self.log.success(f'Started {len(observer_names)} observers. {observer_names}')
        sleep(5)  # To make sure every component has started up correctly

    def run(self):
        """
        test_events = [{'event': 'gcp_mqtt', 'message': 'random data'},
                       {'event': 'device_mqtt', 'message': 'local random data'},
                       {'event': 'device_mqtt', 'message': 'someting data'},
                       {'event': 'device_mqtt', 'message': 'another v data'}]
        """
        events = self.poll_observers()
        events = [{'event': 'gcp_mqtt', 'message': 'random data'}]
        self.notify_observers(events=events)

    def notify_observers(self, events):
        for event in events:
            self.subject.dispatch(**event)

    def poll_observers(self):
        events = []
        for observer in self.observers:
            events.extend(observer.get('obs_object').poll_events())
        return events


if __name__ == '__main__':
    iot_subject = IotSubject()
    iot_subject.run()
