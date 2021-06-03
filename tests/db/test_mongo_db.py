from unittest import mock, TestCase

from pymongo import MongoClient

from home_automation_framework.db.mongo_db import MongoHandler


class MockMongoClient:
    def __init__(self):
        print("hellllo")
        pass


class TestMongoDb(TestCase):

    @mock.patch.object(MongoClient, "__init__")
    def test_connect_to_db_success(self, mock_mongo_client):
        mock_mongo_client.return_value = None
        mongo = MongoHandler("test")

    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_dumy(self, mock_connect):
        mock_connect.return_value = None
        mongo = MongoHandler("test")


