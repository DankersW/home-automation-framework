from unittest import TestCase, mock
from queue import Queue
from threading import Event
from json import dumps

from home_automation_framework.iot_gateway.mqtt_gateway import MqttGateway
#from home_automation_framework.iot_gateway.iot_message import IotMessage
from tests.helper_functions import emtpy_queue


class IotMessage:
    event: str = None
    device_id: str = None
    payload: dict = None


class TestMqttGateway(TestCase):
    test_queue = Queue(10)
    default_event = Event()

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_log_mqtt_traffic(self, mock_mqtt_client):
        """ Testing logging_tests of a mqtt message"""
        mock_mqtt_client.return_value = None
        topic = 'test'
        payload = '1-2-three'
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        emtpy_queue(queue=self.test_queue)
        mqtt_gateway._log_mqtt_traffic(topic=topic, payload=payload)
        result = self.test_queue.get()
        self.assertEqual(result['event'], 'iot_traffic')
        self.assertEqual(result['message']['source'], 'MqttGateway')
        self.assertEqual(result['message']['topic'], topic)
        self.assertEqual(result['message']['payload'], payload)

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_unknown_event(self, mock_mqtt_client):
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        mock_iot_message = IotMessage()
        self.assertIsNone(mqtt_gateway._unknown_event(msg=mock_iot_message))

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_handle_state_change(self, mock_mqtt_client):
        """ Testing handling of a state changed message"""
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        mock_iot_message = IotMessage()
        mock_iot_message.event = 'state'
        mock_iot_message.device_id = 'test_device'
        mock_iot_message.payload = {'state': True}
        emtpy_queue(queue=self.test_queue)
        mqtt_gateway._handle_state_change(msg=mock_iot_message)
        result = self.test_queue.get()
        self.assertEqual(result['event'], 'device_state_changed')
        self.assertEqual(result['message']['device_id'], mock_iot_message.device_id)
        self.assertEqual(result['message']['event_type'], mock_iot_message.event)
        self.assertEqual(result['message']['state'], True)

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_get_message_handler_state_changed(self, mock_mqtt_client):
        """ Testing getting correct handlers """
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        event = 'state'
        handler_name = '_handle_state_change'
        result = mqtt_gateway._select_handler(event=event)
        self.assertEqual(result.__name__, handler_name)

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_get_message_handler_unknown_event(self, mock_mqtt_client):
        """ Testing getting correct handlers """
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        event = 'not_known_event'
        handler_name = '_unknown_event'
        result = mqtt_gateway._select_handler(event=event)
        self.assertEqual(result.__name__, handler_name)

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_on_message_unknown_event(self, mock_mqtt_client):
        """ Testing handling on message e"""
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        topic = 'iot/test_topic'
        data = {'device_id': 'dev_001', 'event_type': 'unknown_event', 'state': True}
        json_data = dumps(data)
        emtpy_queue(queue=self.test_queue)
        mqtt_gateway.on_message(topic=topic, payload=json_data)

        iot_traffic_event = self.test_queue.get()
        self.assertEqual(iot_traffic_event['event'], 'iot_traffic')
        self.assertEqual(iot_traffic_event['message']['source'], 'MqttGateway')
        self.assertEqual(iot_traffic_event['message']['topic'], topic)
        self.assertEqual(iot_traffic_event['message']['payload'], json_data)

        self.assertTrue(self.test_queue.empty())

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_on_message_invalid_payload(self, mock_mqtt_client):
        """ Testing handling on message e"""
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        topic = 'iot/test_topic'
        data = {'device': 'dev_001', 'event_t': 'unknown_event', 'state': True}
        json_data = dumps(data)
        emtpy_queue(queue=self.test_queue)
        mqtt_gateway.on_message(topic=topic, payload=json_data)

        iot_traffic_event = self.test_queue.get()
        self.assertEqual(iot_traffic_event['event'], 'iot_traffic')
        self.assertEqual(iot_traffic_event['message']['source'], 'MqttGateway')
        self.assertEqual(iot_traffic_event['message']['topic'], topic)
        self.assertEqual(iot_traffic_event['message']['payload'], json_data)

        self.assertTrue(self.test_queue.empty())

    @mock.patch("home_automation_framework.iot_gateway.mqtt_client.MqttClient")
    def test_on_connect(self, mock_mqtt_client):
        """ Testing on connect method """
        mock_mqtt_client.return_value = MockMqttClient
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        mqtt_gateway.on_connect()
        self.assertTrue(mqtt_gateway.running)
        self.assertTrue(self.default_event.is_set())


class MockMqttClient:
    @staticmethod
    def subscribe(topics):
        pass
