from queue import Queue
from typing import Callable
from threading import Event

from home_automation_framework.framework.observer_message import ObserverMessage
from home_automation_framework.utils.configuration_parser import ConfigurationParser
from home_automation_framework.iot_gateway.mqtt_gateway import MqttGateway
from home_automation_framework.logging.logging import Logging
from home_automation_framework.db.db_handler import DbHandler
from home_automation_framework.host_health.health_monitor import HealthMonitor
from home_automation_framework.iot_gateway.device_manager import DeviceManager


class Subject:
    def __init__(self, events) -> None:
        self.events = {event: {} for event in events}

    def get_subscribers(self, event) -> dict:
        return self.events[event]

    def register(self, events, obs_object, callback=None) -> None:
        if callback is None:
            callback = getattr(obs_object, 'notify')
        for event in events:
            self.get_subscribers(event)[obs_object] = callback

    def unregister(self, event, obs_object) -> None:
        del self.get_subscribers(event)[obs_object]

    def dispatch(self, message) -> None:
        for _, callback in self.get_subscribers(message.event).items():
            callback(message)


class IotSubject:
    observers = []
    running = False

    def __init__(self) -> None:
        self.log = Logging(owner=__file__, config=True)
        self.config = ConfigurationParser().get_config()

        events = self.config['framework']['events']
        self.subject = Subject(events)

        self.observer_queue = Queue(maxsize=100)
        self._thread_started_event = Event()

        self.init_observers()
        self.attach_observers()
        self.start_observer_threats()

    def init_observers(self) -> None:
        active_components = self._get_activated_components()
        for component in active_components:
            obj = self._get_matching_object(component_name=component)
            observer = obj(queue=self.observer_queue, thread_event=self._thread_started_event)
            events = observer.subscribed_event
            self.observers.append({'obs_object': observer, 'events': events})

    def _get_activated_components(self) -> list:
        system_components = self.config['system_components'].keys()
        return [component for component in system_components if self.config['system_components'][component]]

    @staticmethod
    def _get_matching_object(component_name: str) -> Callable:
        object_mapper = {
            'mqtt_gateway': MqttGateway,
            'db': DbHandler,
            'host_monitor': HealthMonitor,
            'device_manager': DeviceManager
        }
        return object_mapper.get(component_name)

    def attach_observers(self) -> None:
        for observer in self.observers:
            self.subject.register(**observer)

    def start_observer_threats(self) -> None:
        for observer in self.observers:
            observer.get('obs_object').start()
            self._thread_started_event.wait()
        observer_names = [key['obs_object'] for key in self.observers]
        self.log.success(f'Started {len(observer_names)} observers. {observer_names}')
        self.running = True

    def run(self) -> None:
        while self.running:
            msg = self.get_observer_events()
            self.notify_observers(msg=msg)

    def notify_observers(self, msg: ObserverMessage) -> None:
        self.subject.dispatch(message=msg)

    def get_observer_events(self) -> ObserverMessage:
        return self.observer_queue.get()
