from dataclasses import dataclass

from pymongo import MongoClient, errors

from lib.configuration_parser import ConfigurationParser
from src.logging.logging import Logging


class DbDriver:
    def __init__(self):
        mongo = MongoDriver

    def __del__(self):
        pass


class MongoDriver:
    @dataclass
    class MongoConfCloud:
        admin_pwd: str = 'testlabadmin'
        db: str = 'home_automation'
        url: str = f'mongodb+srv://admin:{admin_pwd}@cluster0.jedhb.gcp.mongodb.net/{db}?retryWrites=true&w=majority'

    @dataclass
    class MongoConfLocal:
        host: str = 'host_ip'
        user: str = 'admin'
        pwd: str = 'mongo_admin_iot'
        db: str = 'iot_db'
        url: str = f'mongodb://{user}:{pwd}@{host}/'

    def __init__(self):
        self.config = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)

        self.mongo_db = self.connect_to_db()

    def connect_to_db(self):
        mongo_host = self.config['mongo_db']['host_ip']
        mongo_url = self.MongoConfLocal.url.replace(self.MongoConfLocal.host, mongo_host)

        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=30)
            client.server_info()
            db = client[self.MongoConfLocal.db]
            self.log.success(f'Connected to MongoDB {self.MongoConfLocal.db!r} at {mongo_url}')
        except errors.ServerSelectionTimeoutError as err:
            self.log.critical(f'Connection MongoDB error at {mongo_url} with error: {err}')
            raise RuntimeError
        return db

    def insert(self):
        db = self.client.home_automation
        collection = db.deviceStates
        test_data = {
            'device_name': 'hello_world',
            'state': '1'
        }
        result = collection.insert_one(test_data)
        print(f'result: {result.inserted_id}')

    def update(self):
        pass

    def retrieve(self):
        db = self.client.home_automation
        collection = db.deviceStates
        query_result = collection.find({'device_name': 'hello_world'})
        for i, item in enumerate(query_result):
            print(f'{i}: {item}')

    def get_all_collections(self):
        pass

    def get_all_documents(self, collection):
        pass

    def get_all_objects(self, document):
        pass

    def find_queury(self, collection, document):
        pass

    def update_object(self):
        pass


if __name__ == '__main__':
    db = MongoDriver()
