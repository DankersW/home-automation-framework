from unittest import mock, TestCase
from enum import Enum
from pymongo import MongoClient

from home_automation_framework.db.mongo_db import MongoHandler


class MockMongoClient(Enum):
    db_name = "name"

    def __init__(self, _):
        print("hellllo")
        pass

    @staticmethod
    def server_info():
        print("pass")


class TestMongoDb(TestCase):

    @mock.patch.object(MongoHandler, "get_mongo_client")
    def test_connect_to_db_success(self, mock_mongo_client):
        mock_mongo_client.return_value = MockMongoClient
        mongo = MongoHandler("db_name")



    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_dumy(self, mock_connect):
        mock_connect.return_value = None
        mongo = MongoHandler("test")


