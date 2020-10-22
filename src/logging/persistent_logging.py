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

        collection_list = self.get_all_collections(db=db)
        if collection_list == None:

        print(f'colelctions: {collection_list}')

        return db

    @staticmethod
    def get_all_collections(db):
        return db.list_collection_names()

    def get_collection_name(self):


    def generate_collection_name(self, current_time):
        collection_base_name = self.config['logging']['log_collection']
        dt = current_time.strftime('%Y%m%d%H%M')
        return f'{collection_base_name}_{dt}'

    def log(self, data):
        print(f'log{data}')


if __name__ == '__main__':
    db_pres = DbLogging()
    db_pres.connect_to_db()
