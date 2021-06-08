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
            action(msg=item)

    def notify(self, msg: ObserverMessage) -> None:
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

    def get_document_data(self, document: str) -> list:
        return self.mongo.get(collection_name=document)

    def store_state_data(self, msg: ObserverMessage) -> None:
        document_data = {'device_id': msg.data.get('device_id'), 'event': msg.event,
                         'change_source': msg.data.get('event'), 'state': msg.data.get('state')}
        self.mongo.write(collection_name="states", data=document_data, key="device_id")

    def add_document_row(self, msg: ObserverMessage) -> None:
        self.mongo.insert(collection_name=msg.event, data=msg.data)

    def handle_digital_twin(self, msg: ObserverMessage) -> None:
        if msg.subject == "fetch_digital_twin":
            self._fetch_digital_twin()
        elif msg.subject == "save_digital_twin":
            self._save_digital_twin(twin=msg.data)
        else:
            self.action_skip()

    def _fetch_digital_twin(self) -> None:
        self.log.info("Fetching digital twin from DB")
        twin_data = self.get_document_data(document="digital_twin")
        digital_twin = self._outbound_adapter(data=twin_data)
        msg = ObserverMessage(event="digital_twin", data=digital_twin, subject="retrieved_digital_twin")
        self.observer_publish_queue.put(msg)

    def _save_digital_twin(self, twin: list) -> None:
        self.log.info("Uploading updated digital twin")
        self.mongo.write(collection_name='digital_twin', data=twin, key='device_name')

    @staticmethod
    def _outbound_adapter(data: list) -> list:
        """ Removes the object_id field from each data entry, preping the data for transportation """
        for entry in data:
            entry.pop("_id", None)
        return data
