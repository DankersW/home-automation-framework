from threading import Thread, Event
from queue import Queue
from typing import Callable

from home_automation_framework.framework.observer_message import ObserverMessage
from home_automation_framework.db.mongo_db import MongoHandler
from home_automation_framework.logging.logging import Logging


class DbHandler(Thread):
    running = True
    subscribed_event = ['gcp_state_changed', 'device_state_changed', 'iot_traffic', 'host_health', 'device_sensor_data',
                        'digital_twin']

    def __init__(self, queue: Queue, thread_event: Event) -> None:
        Thread.__init__(self)
        self.mongo = MongoHandler(db_name='iot_db')
        self.observer_publish_queue = queue
        self._thread_ready = thread_event
        self.observer_notify_queue = Queue(maxsize=100)
        self.log = Logging(owner=__file__, config=True)

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        self._thread_ready.set()
        while self.running:
            item = self.observer_notify_queue.get()
            action = self.action_selector(event=item.event)
            action(event=item.event, msg=item)

    def notify(self,  event: str, msg: ObserverMessage) -> None:
        self.observer_notify_queue.put(msg)

    def action_selector(self, event: str) -> Callable:
        action_map = {'gcp_state_changed': self.store_state_data,
                      'device_state_changed': self.store_state_data,
                      'iot_traffic': self.add_document_row,
                      'host_health': self.add_document_row,
                      'device_sensor_data': self.add_document_row,
                      'digital_twin': self.handle_digital_twin}
        return action_map.get(event, self.action_skip)

    @staticmethod
    def action_skip():
        pass

    def get_data(self, document: str, ) -> list:
        return self.mongo.get(collection_name=document)

    def store_state_data(self, event: str, msg: ObserverMessage) -> None:
        object_id = self.mongo.check_existence_by_device_name('states', msg.data.get('device_id'))
        if object_id:
            updated_data = {'$set': {'state': msg.data.get('state'), 'event': event,
                                     'change_source': msg.data.get('event_type')}}
            self.mongo.update_object(collection_name='states', object_id=object_id, updated_values=updated_data)
        else:
            document_data = {'device_id': msg.data.get('device_id'), 'event': event, 'change_source': msg.data.get('event'),
                             'state': msg.data.get('state')}
            self.mongo.insert(collection_name='states', data=document_data)

    def add_document_row(self, event: str, msg: ObserverMessage) -> None:
        self.mongo.insert(collection_name=event, data=msg.data)

    def handle_digital_twin(self, event: str, msg: ObserverMessage) -> None:
        if msg.subject == "fetch_digital_twin":
            self.log.info("Fetching digital twin from DB")
            digital_twin = self.get_data(document="digital_twin")
            msg = ObserverMessage(event="digital_twin", data=digital_twin, subject="retrieved_digital_twin")
            self.observer_publish_queue.put(msg)
        elif msg.subject == "update_digital_twin":
            pass
        elif msg.subject == "retrieved_digital_twin":
            pass
        else:
            self.log.error(f"Unsupported action type {msg.subject}, from event {event}")



