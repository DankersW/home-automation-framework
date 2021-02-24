from unittest import TestCase, mock
from threading import Event
from queue import Queue

from home_automation_framework.db.db_handler import DbHandler
from home_automation_framework.db.mongo_db import MongoHandler


class MockMongo:
    def __init__(self, db_name):
        print(db_name)

    def get(self, collection_name, device_name=None):
        return ['a', 'b']

    @staticmethod
    def insert(collection_name, data):
        pass


class TestDbHandler(TestCase):
    test_queue = Queue(10)
    test_event = Event()

    def test_subscribed_events(self):
        events = ['gcp_state_changed', 'device_state_changed', 'iot_traffic', 'host_health', 'device_sensor_data']
        _events = DbHandler.subscribed_event
        self.assertEqual(_events, events)

    def test_initial_running_state(self):
        self.assertTrue(DbHandler.running)

    @mock.patch.object(MongoHandler, '__init__')
    def test_init(self, mock_mongo):
        mock_mongo.return_value = None
        _ = DbHandler(queue=self.test_queue, thread_event=self.test_event)

    @mock.patch.object(MongoHandler, '__init__')
    def test_notify(self, mock_mongo):
        mock_mongo.return_value = None
        db_handler = DbHandler(queue=self.test_queue, thread_event=self.test_event)
        msg = {'test': 123}
        event = 'test'
        db_handler.notify(msg=msg, event=event)
        queue_item = db_handler.observer_notify_queue.get()
        self.assertDictEqual(queue_item, {'event': 'test', 'msg': {'test': 123}})

    @mock.patch.object(MongoHandler, '__init__')
    def test_action_selector(self, mock_mongo):
        actions = {'gcp_state_changed': 'store_state_data',
                   'device_state_changed': 'store_state_data',
                   'iot_traffic': 'add_document_row',
                   'host_health': 'add_document_row',
                   'device_sensor_data': 'add_document_row',
                   'does_not_exist': 'action_skip'}
        mock_mongo.return_value = None
        db_handler = DbHandler(queue=self.test_queue, thread_event=self.test_event)
        for action in actions.keys():
            handler = db_handler.action_selector(event=action).__name__
            self.assertEqual(handler, actions[action])

    @mock.patch.object(MongoHandler, '__init__')
    def test_get_data(self, mock_mongo):
        mock_mongo.return_value = None
        db_handler = DbHandler(queue=self.test_queue, thread_event=self.test_event)
        db_handler.mongo = MockMongo
        db_handler.get_data()

    @mock.patch.object(MongoHandler, '__init__')
    def test_add_document_row(self, mock_mongo):
        mock_mongo.return_value = None
        db_handler = DbHandler(queue=self.test_queue, thread_event=self.test_event)
        db_handler.mongo = MockMongo
        db_handler.add_document_row(event='pass', data={})
