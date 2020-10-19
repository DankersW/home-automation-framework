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

    def get_data(self):
        print(self.mongo.get('states', 'test_device'))

    def store_data(self):
        device_exists = self.mongo.check_existence_by_device_name('states', 'test_device_')
        if device_exists:
            pass
        else:
            pass


if __name__ == '__main__':
    db_handler = DbHandler()
    #db_handler.get_data()
    db_handler.store_data()
