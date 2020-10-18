from dataclasses import dataclass

from pymongo import MongoClient, errors

from lib.configuration_parser import ConfigurationParser


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
        url: str = f'mongodb://{user}:{pwd}@{host}/{db}'

    def __init__(self):
        self.config = ConfigurationParser().get_config()

        self.mongo_client = self.connect_to_db()

    def connect_to_db(self):
        mongo_host = self.config['mongo_db']['host_ip']
        mongo_url = self.MongoConfLocal.url.replace(self.MongoConfLocal.host, mongo_host)

        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=10)
            client.server_info()  # force connection on a request as the
            # connect=True parameter of MongoClient seems
            # to be useless here
        except errors.ServerSelectionTimeoutError as err:
            # do whatever you need
            print(err)

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
