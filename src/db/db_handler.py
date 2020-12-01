from threading import Thread
from queue import Queue

from src.db.mongo_db import MongoHandler


class DbHandler(Thread):
    running = True

    def __init__(self, queue: Queue) -> None:
        Thread.__init__(self)
        self.mongo = MongoHandler(db_name='iot_db')
        self.received_queue = queue
        self.to_handle_queue = Queue(maxsize=100)

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            item = self.to_handle_queue.get()
            state_change = item.get('event') == 'gcp_state_changed' or item.get('event') == 'device_state_changed'
            if state_change:
                self.store_state_data(event=item.get('event'), data=item.get('msg'))
            elif item.get('event') == 'iot_traffic':
                # todo: handle traffic
                print(item)

    def notify(self, msg: dict, event: str) -> None:
        self.to_handle_queue.put({'event': event, 'msg': msg})

    def get_data(self, device_name: str = None) -> None:
        data = self.mongo.get('states', device_name)
        for item in data:
            print(item)

    def store_state_data(self, event: str, data: dict) -> None:
        object_id = self.mongo.check_existence_by_device_name('states', data.get('device_id'))
        if object_id:
            updated_data = {'$set': {'state': data.get('state'), 'event': event, 'change_source': data.get('event')}}
            self.mongo.update_object(collection_name='states', object_id=object_id, updated_values=updated_data)
        else:
            document_data = {'device_id': data.get('device_id'), 'event': event, 'change_source': data.get('event'),
                             'state': data.get('state')}
            self.mongo.insert(collection_name='states', data=document_data)


if __name__ == '__main__':
    t_queue = Queue(10)
    db_handler = DbHandler(queue=t_queue)
    db_handler.get_data()
