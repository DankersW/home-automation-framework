from threading import Thread
from time import sleep

from src.db.mongo_db import MongoHandler


class DbHandler(Thread):
    running = True

    def __init__(self):
        Thread.__init__(self)
        self.mongo = MongoHandler(db_name='iot_db')

    def __del__(self):
        self.running = False

    def run(self):
        while self.running:
            sleep(0.1)

    def notify(self, msg, event):
        # todo: handle data and call store method
        print(f"db_handler: notified - {msg} - {event}")
        self.store_data(msg)

    @staticmethod
    def poll_events():
        return []

    def get_data(self, device_name=None):
        data = self.mongo.get('states', device_name)
        for item in data:
            print(item)

    def store_data(self, data):
        device_name = data.get('device')
        device_id = self.mongo.check_existence_by_device_name('states', device_name)
        if device_id:
            updated_data = {'$set': {'state': data.get('state')}}
            self.mongo.update_object('states', device_id, updated_data)
        else:
            self.mongo.insert('states', data)


if __name__ == '__main__':
    db_handler = DbHandler()
    db_handler.get_data()
    test_data = {'device': 'light_switch_2', 'location': 'living-room', 'state': False}
    db_handler.store_data(test_data)
