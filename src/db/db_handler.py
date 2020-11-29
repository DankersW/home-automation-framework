from threading import Thread
from queue import Queue

from src.db.mongo_db import MongoHandler


class DbHandler(Thread):
    running = True

    def __init__(self, queue):
        Thread.__init__(self)
        self.mongo = MongoHandler(db_name='iot_db')
        self.received_queue = queue
        self.to_handle_queue = Queue(maxsize=100)

    def __del__(self):
        self.running = False

    def run(self):
        while self.running:
            item = self.to_handle_queue.get()
            print(f'new event - {item}')
            if item.get('event') == 'gcp_state_changed' or item.get('event') == 'device_state_changed':

                self.store_state_data(data=item.get('msg'))

    def notify(self, msg, event):
        self.to_handle_queue.put({'event': event, 'msg': msg})

    def get_data(self, device_name=None):
        data = self.mongo.get('states', device_name)
        for item in data:
            print(item)

    def store_state_data(self, data):
        print(f'storing data: {data}')
        device_id = self.mongo.check_existence_by_device_name('states', data.get('device_id'))
        if device_id:
            updated_data = {'$set': {'state': data.get('payload')}}
            self.mongo.update_object('states', device_id, updated_data)
        else:
            self.mongo.insert('states', data)


if __name__ == '__main__':
    t_queue = Queue(10)
    db_handler = DbHandler(queue=t_queue)
    db_handler.get_data()
    test_data = {'device': 'light_switch_2', 'location': 'living-room', 'state': False}
    db_handler.store_state_data(test_data)
