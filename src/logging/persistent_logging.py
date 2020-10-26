from dataclasses import dataclass
from datetime import datetime

from pymongo import MongoClient, errors

from lib.configuration_parser import ConfigurationParser


class DbLogging:
    @dataclass
    class MongoConfLocal:
        host: str = 'host_ip'
        user: str = 'admin'
        pwd: str = 'mongo_admin_iot'
        url: str = f'mongodb://{user}:{pwd}@{host}/'

    def __init__(self):
        self.config = ConfigurationParser().get_config()
        self.collection = None
        self.mongo_db = None

    def connect(self):
        mongo_host = self.config['mongo_db']['host_ip']
        mongo_url = self.MongoConfLocal.url.replace(self.MongoConfLocal.host, mongo_host)

        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=30)
            client.server_info()
            db = client['logs']
        except errors.ServerSelectionTimeoutError as error:
            raise RuntimeError from error

        self.collection = self.get_collection(db=db)
        self.mongo_db = db

    def get_collection(self, db):
        collection_list = self.get_all_collections(db=db)
        already_logging, collection_name = self.already_logging(collection_list)
        if collection_list is None or not already_logging:
            collection_name = self.generate_collection_name(current_time=datetime.now())
            db.create_collection(name=collection_name)
        return collection_name

    @staticmethod
    def get_all_collections(db):
        return db.list_collection_names()

    @staticmethod
    def already_logging(collection_list):
        name = f'logs_{datetime.now().strftime("%Y%m%d%H%M")}'
        if name in collection_list:
            return True, name
        return False, None

    def generate_collection_name(self, current_time):
        collection_base_name = self.config['logging']['log_collection_name']
        dt = current_time.strftime('%Y%m%d%H%M')
        return f'{collection_base_name}_{dt}'

    def log(self, source, time, log_lvl, msg):
        data = {'timestamp': time, 'source': source, 'log_lvl': log_lvl, 'msg': msg}
        collection = self.mongo_db[self.collection]
        collection.insert_one(data)


if __name__ == '__main__':
    db_pres = DbLogging()
    db_pres.connect()
    data_test = {'time': '2020-10-22 14:55', 'source': 'logging', 'log_lvl': 'info', 'msg': 'test'}
    db_pres.log(**data_test)
