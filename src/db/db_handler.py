from dataclasses import dataclass

from pymongo import MongoClient, errors

from lib.configuration_parser import ConfigurationParser
from src.logging.logging import Logging
from src.db.mongo_db import MongoHandler


class DbHandler:
    def __init__(self):
        self.mongo = MongoHandler()

    def __del__(self):
        pass

    def get_historical_data(self):
        print("Call to historical db")

    def set_historical_data(self, data):
        pass

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
    data = {'device': 'light_switch_2', 'location': 'living', 'state': False}
    db_handler.store_data(data)
