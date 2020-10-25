from dataclasses import dataclass
from datetime import datetime

from pymongo import MongoClient, errors

from lib.configuration_parser import ConfigurationParser


# todo: connect to log db

# todo: create a new document name that has current timestamp as name

# todo: if document name, time difference is less then 1 use that name else create a new document. in this all
#  write to the same log

# todo: data structure: time, name, log level, info


class DbLogging:
    @dataclass
    class MongoConfLocal:
        host: str = 'host_ip'
        user: str = 'admin'
        pwd: str = 'mongo_admin_iot'
        url: str = f'mongodb://{user}:{pwd}@{host}/'

    def __init__(self):
        self.config = ConfigurationParser().get_config()
        self.db = None
        self.collection = None

    def connect_to_db(self):
        mongo_host = self.config['mongo_db']['host_ip']
        mongo_url = self.MongoConfLocal.url.replace(self.MongoConfLocal.host, mongo_host)

        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=30)
            client.server_info()
            db = client['logs']
            print(f'Connected to MongoDB logs at {mongo_url}')
        except errors.ServerSelectionTimeoutError as err:
            print(f'Connection MongoDB error at {mongo_url} with error: {err}')
            raise RuntimeError

        self.collection = self.get_collection(db=db)
        self.db = db
        return db

    def get_collection(self, db):
        collection_list = self.get_all_collections(db=db)
        already_logging, collection_name = self.already_logging(collection_list)
        if collection_list is None or not already_logging:
            collection_name = self.generate_collection_name(current_time=datetime.now())
            db.create_collection(name=collection_name)
        print(f'colelctions: {collection_list}')
        print(f'colelction: {collection_name}')
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
        collection_base_name = self.config['logging']['log_collection']
        dt = current_time.strftime('%Y%m%d%H%M')
        return f'{collection_base_name}_{dt}'

    def abc(self, source, time, log_lvl, msg):
        data = {'timestamp': time, 'source': source, 'log_lvl': log_lvl, 'msg': msg}
        collection = self.db[self.collection]
        data_id = collection.insert_one(data)
        print(f'log{data} - {data_id}')


if __name__ == '__main__':
    db_pres = DbLogging()
    db_pres.connect_to_db()
    data_test = {'time': '2020-10-22 14:55', 'source': 'logging', 'log_lvl': 'info', 'msg': 'test'}
    db_pres.abc(**data_test)
