from dataclasses import dataclass

from pymongo import MongoClient, errors

from lib.configuration_parser import ConfigurationParser
from src.logging.logging import Logging


class MongoHandler:
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
        url: str = f'mongodb://{user}:{pwd}@{host}/'

    def __init__(self, db_name):
        self.config = ConfigurationParser().get_config()
        self.log = Logging(owner=__file__, config=True)
        self.mongo_db = self.connect_to_db(db_name=db_name)

    def connect_to_db(self, db_name):
        mongo_host = self.config['mongo_db']['host_ip']
        mongo_url = self.MongoConfLocal.url.replace(self.MongoConfLocal.host, mongo_host)

        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=30)
            client.server_info()
            db = client[db_name]
            self.log.success(f'Connected to MongoDB {db_name!r} at {mongo_url}')
        except errors.ServerSelectionTimeoutError as err:
            self.log.critical(f'Connection MongoDB error at {mongo_url} with error: {err}')
            raise RuntimeError
        return db

    def get(self, collection_name, device_name=None):
        collection = self.mongo_db[collection_name]
        query = {}
        if device_name:
            query.update({'device': device_name})
        self.log.info(f'Executing query {query!r} on collection {collection_name!r}')
        return list(collection.find(query))

    def insert(self, collection_name, data):
        collection = self.mongo_db[collection_name]
        data_id = collection.insert_one(data)
        self.log.info(f'Inserted {data!r} into {collection_name!r} with ID {data_id}')

    def update_object(self, collection_name, device_id, updated_values):
        collection = self.mongo_db[collection_name]
        query = {'_id': device_id}
        collection.update_one(query, updated_values)
        self.log.info(f'Data with ID {device_id!r} in collection {collection_name!r} updated successfully')

    def check_existence_by_device_name(self, collection_name, device_name):
        collection = self.mongo_db[collection_name]
        query = {'device': device_name}
        data = collection.find_one(query)
        # if type(data) == dict:
        if isinstance(data, dict):
            return data.get('_id')
        return None


if __name__ == '__main__':
    t_db = MongoHandler(db_name='iot_db')
    print(t_db.get('states', 'test_device'))
