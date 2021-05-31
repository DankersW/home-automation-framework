from dataclasses import dataclass
from typing import Union

from pymongo import MongoClient, errors

from home_automation_framework.utils.configuration_parser import ConfigurationParser
from home_automation_framework.logging.logging import Logging


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
            client = MongoClient(mongo_url)
            client.server_info()
            db = client[db_name]
            self.log.success(f'Connected to MongoDB {db_name!r} at {mongo_url}')
        except errors.ServerSelectionTimeoutError as err:
            self.log.critical(f'Connection MongoDB error at {mongo_url} with error: {err}')
            raise RuntimeError from err
        return db

    def get(self, collection_name, query: dict = None) -> list:
        collection = self.mongo_db[collection_name]
        self.log.debug(f'Executing query {query!r} on collection {collection_name!r}')
        return list(collection.find(query))

    def insert(self, collection_name, data):
        collection = self.mongo_db[collection_name]
        data_id = collection.insert_one(data)
        self.log.debug(f'Inserted {data!r} into {collection_name!r} with ID {data_id}')

    def update(self, collection_name, object_id, updated_values):
        collection = self.mongo_db[collection_name]
        query = {'_id': object_id}
        collection.update_one(query, updated_values)
        self.log.debug(f'Data with ID {object_id!r} in collection {collection_name!r} updated successfully')

    def write(self, collection_name: str, data: Union[list, dict], key: str):
        """ Add's data if it does not exist, else update that data based on key """

        # todo unpack list

    def _write(self, collection: str, data: dict, key: str):
        pass
        _id = self.check_existence_by_query(collection_name=collection_name, check_existence)


    def check_existence_by_query(self, collection_name: str, query: dict) -> Union[str, None]:
        collection = self.mongo_db[collection_name]
        data = collection.find_one(query)
        if isinstance(data, dict):
            return data.get('_id')
        return None
