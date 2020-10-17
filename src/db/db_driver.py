from dataclasses import dataclass

from pymongo import MongoClient

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
        host: str = ''
        user: str = 'admin'
        pwd: str = 'mongo_admin_iot'
        db: str = 'iot_db'

    def __init__(self):
        self.config = ConfigurationParser().get_config()

        self.client = MongoClient(self.MongoConf.url)

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


if __name__ == '__main__':
    db = MongoDriver()
