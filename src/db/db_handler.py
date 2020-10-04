from dataclasses import dataclass

from pymongo import MongoClient

from lib.configuration_parser import ConfigurationParser


class DbHandler:
    def get(self, query):
        pass

    def write(self, data):
        pass


class MongoDbHandler:
    @dataclass
    class MongoConf:
        admin_pwd: str = 'testlabadmin'
        db: str = 'home_automation'
        url: str = f'mongodb+srv://admin:{admin_pwd}@cluster0.jedhb.gcp.mongodb.net/{db}?retryWrites=true&w=majority'

    def __init__(self):
        self.config = ConfigurationParser().get_config()

        self.client = MongoClient(self.MongoConf.url)
        self.insert()
        self.retrieve()
        print('done')

    def __del__(self):
        print('close')
        print('after close')

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
    db = MongoDbHandler()
