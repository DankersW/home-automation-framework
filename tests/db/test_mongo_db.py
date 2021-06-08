from unittest import mock, TestCase
from enum import Enum
from pymongo import errors

from home_automation_framework.db.mongo_db import MongoHandler


class MockCollection:
    @staticmethod
    def find(query):
        return 1


class MockMongoClient(Enum):
    db_name = "name"
    mock_collection = MockCollection()

    saved_data = None

    def __init__(self, _):
        pass

    @staticmethod
    def server_info():
        pass

    @staticmethod
    def find(query):
        return [1, 2, 3]

    @staticmethod
    def find_one(_):
        return {'_id': "1"}

    def insert_one(self, data):
        self.saved_data = data

    @staticmethod
    def update_one(_, __):
        pass


class MockMongoClientFail:
    def __init__(self, _):
        pass

    @staticmethod
    def server_info():
        raise errors.ServerSelectionTimeoutError


class MockMongoClientFindOne(Enum):
    db_name = "name"
    mock_collection = MockCollection()

    def __init__(self, _):
        pass

    @staticmethod
    def find_one(_):
        return None


class TestMongoDb(TestCase):

    @mock.patch.object(MongoHandler, "get_mongo_client")
    def test_connect_to_db_success(self, mock_mongo_client):
        mock_mongo_client.return_value = MockMongoClient
        db = MongoHandler("db_name")
        print(db.__class__.__name__)
        self.assertEqual(db.__class__.__name__, "MongoHandler")

    @mock.patch.object(MongoHandler, "get_mongo_client")
    def test_connect_to_db_fail(self,  mock_mongo_client):
        mock_mongo_client.return_value = MockMongoClientFail
        try:
            _ = MongoHandler("db_name")
        except RuntimeError:
            self.assertTrue(1)
        else:
            self.assertTrue(0)

    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_get(self, mock_connect):
        mock_connect.return_value = MockMongoClient
        mongo = MongoHandler("db_name")
        result = mongo.get(collection_name="mock_collection", query={"abc": 123})
        self.assertListEqual(result, [1, 2, 3])

    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_insert(self, mock_connect):
        mock_connect.return_value = MockMongoClient
        mongo = MongoHandler("db_name")
        mongo.insert(collection_name="mock_collection", data={"abc": 123})
        self.assertTrue(1)

    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_update(self, mock_connect):
        mock_connect.return_value = MockMongoClient
        mongo = MongoHandler("db_name")
        mongo.update(collection_name="mock_collection", object_id="", updated_values={"abc": 123})
        self.assertTrue(1)

    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_get_first_object_id_from_query(self, mock_connect):
        mock_connect.return_value = MockMongoClient
        mongo = MongoHandler("db_name")
        result = mongo.get_first_object_id_from_query(collection_name="mock_collection",query={"abc": 123})
        self.assertEqual(result, "1")

    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_get_first_object_id_from_query_fail(self, mock_connect):
        mock_connect.return_value = MockMongoClientFindOne
        mongo = MongoHandler("db_name")
        result = mongo.get_first_object_id_from_query(collection_name="mock_collection", query={"abc": 123})
        self.assertIsNone(result)

    @mock.patch.object(MongoHandler, "_write")
    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_write(self, mock_connect, mock_write):
        mock_connect.return_value = MockMongoClient
        mock_write.return_value = None
        mongo = MongoHandler("db_name")
        mongo.write("", {}, "")
        self.assertTrue(1)

    @mock.patch.object(MongoHandler, "_write")
    @mock.patch.object(MongoHandler, "connect_to_db")
    def test_write_list(self, mock_connect, mock_write):
        mock_connect.return_value = MockMongoClient
        mock_write.return_value = None
        mongo = MongoHandler("db_name")
        mongo.write("", [], "")
        self.assertTrue(1)

    @mock.patch.object(MongoHandler, "get_first_object_id_from_query")
    @mock.patch.object(MongoHandler, "insert")
    @mock.patch.object(MongoHandler, "connect_to_db")
    def test__write_insert(self, mock_connect, mock_insert, mock_query):
        mock_connect.return_value = MockMongoClient
        mock_insert.return_value = None
        mock_query.return_value = None
        mongo = MongoHandler("db_name")
        mongo._write("", {}, "")
        self.assertTrue(mock_insert.called)

    @mock.patch.object(MongoHandler, "get_first_object_id_from_query")
    @mock.patch.object(MongoHandler, "update")
    @mock.patch.object(MongoHandler, "connect_to_db")
    def test__write_update(self, mock_connect, mock_update, mock_query):
        mock_connect.return_value = MockMongoClient
        mock_update.return_value = None
        mock_query.return_value = True
        mongo = MongoHandler("db_name")
        mongo._write("", {}, "")
        self.assertTrue(mock_update.called)
