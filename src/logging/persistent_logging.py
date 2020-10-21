from dataclasses import dataclass

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

    def __init__(self, document_name):
        self.config = ConfigurationParser().get_config()
        print(f'init-{document_name}')

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

        return db

    def generate_document_name(self):
        document_base_name = self.config['logging']['log_document']
        print(f'base name {document_base_name!r}')

    def log(self, data):
        print(f'log{data}')
