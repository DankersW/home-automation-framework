import time
from threading import Thread, Event
from queue import Queue
from typing import Callable

from home_automation_framework.framework.observer_message import ObserverMessage
from home_automation_framework.db.mongo_db import MongoHandler
from home_automation_framework.logging.logging import Logging

# todo: move more logic into the mongo db
# todo: let mongo except list and let it check if stuff already excist


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
            print("waiting")
            item = self.observer_notify_queue.get()
            print(item)
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

    def get_data(self, document: str, ) -> list:
        return self.mongo.get(collection_name=document)

    # todo
    def store_state_data(self, msg: ObserverMessage) -> None:
        query = {'device_id': msg.data.get('device_id')}
        object_id = self.mongo.check_existence_by_query(collection_name='states', query=query)
        if object_id:
            updated_data = {'$set': {'state': msg.data.get('state'), 'event': msg.event,
                                     'change_source': msg.data.get('event_type')}}
            self.mongo.update(collection_name='states', object_id=object_id, updated_values=updated_data)
        else:
            document_data = {'device_id': msg.data.get('device_id'), 'event': msg.event,
                             'change_source': msg.data.get('event'),
                             'state': msg.data.get('state')}
            self.mongo.insert(collection_name='states', data=document_data)

    def add_document_row(self, msg: ObserverMessage) -> None:
        self.mongo.insert(collection_name=msg.event, data=msg.data)

    # todo
    def handle_digital_twin(self, msg: ObserverMessage) -> None:
        action = self.get_digital_twin_action(sub_event=msg.subject)
        action(msg.data)

    # todo: combine with above
    def get_digital_twin_action(self, sub_event: str) -> Callable:
        action_map = {
            "fetch_digital_twin": self._fetch_digital_twin,
            "save_digital_twin": self._save_digital_twin
        }
        return action_map.get(sub_event, self.action_skip)

    def _fetch_digital_twin(self, _) -> None:
        self.log.info("Fetching digital twin from DB")
        digital_twin = self.get_data(document="digital_twin")
        msg = ObserverMessage(event="digital_twin", data=digital_twin, subject="retrieved_digital_twin")
        self.observer_publish_queue.put(msg)

    # todo: remove object_id from all data we send out, publish adapter
    def _save_digital_twin(self, twin: list) -> None:
        self.log.info("Uploading updated digital twin")
        self.mongo.write(collection_name='digital_twin', data=twin, key='device_name')


if __name__ == '__main__':
    queue = Queue(10)
    event = Event()
    db_handler = DbHandler(queue=queue, thread_event=event)
    twin = [{'_id': "ObjectId('6089b77907384800073936a6')", 'device_name': 'test_device', 'active': False, 'location': 'on-desk', 'technology': 'WI-FI', 'battery_level': 'USB-power'}]
    db_handler._save_digital_twin(twin)
