from unittest import TestCase, mock
from queue import Queue
from threading import Event
from json import dumps

from src.iot_gateway.mqtt_gateway import MqttGateway
from tests.helper_functions import emtpy_queue


class TestMqttGateway(TestCase):
    test_queue = Queue(10)
    default_event = Event()

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_log_mqtt_traffic(self, mock_mqtt_client):
        """ Testing logging of a mqtt message"""
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

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_parse_mqtt_payload_correct(self, mock_mqtt_client):
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        payload = {'test': 123}
        result = mqtt_gateway._parse_mqtt_payload(payload=dumps(payload))
        self.assertEqual(result, payload)

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_parse_mqtt_payload_incorrect(self, mock_mqtt_client):
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        result = mqtt_gateway._parse_mqtt_payload(payload='payload')
        self.assertEqual(result, dict())

    def test_is_valid_mqtt_message_correct(self):
        message = {'device_id': 'device_001', 'event_type': 'iot_dev_state_change', 'state': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertTrue(result)

    def test_is_valid_mqtt_message_device_id_missing(self):
        message = {'device_': 'device_001', 'event_type': 'iot_dev_state_change', 'state': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertFalse(result)

    def test_is_valid_mqtt_message_event_type_missing(self):
        message = {'device_id': 'device_001', 'event_t': 'iot_dev_state_change', 'state': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertFalse(result)

    def test_is_valid_mqtt_message_state_missing(self):
        message = {'device_id': 'device_001', 'event_type': 'iot_dev_state_change', 'state_': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertFalse(result)

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_unknown_event(self, mock_mqtt_client):
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        self.assertIsNone(mqtt_gateway._unknown_event(data=dict()))

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_handle_state_change(self, mock_mqtt_client):
        """ Testing handling of a state changed message"""
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        data = {'device_id': 1, 'event_type': 2, 'state': True}
        emtpy_queue(queue=self.test_queue)
        mqtt_gateway._handle_state_change(data=data)
        result = self.test_queue.get()
        self.assertEqual(result['event'], 'device_state_changed')
        self.assertEqual(result['message']['device_id'], data.get('device_id'))
        self.assertEqual(result['message']['event_type'], data.get('event_type'))
        self.assertEqual(result['message']['state'], data.get('state'))

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_get_message_handler_state_changed(self, mock_mqtt_client):
        """ Testing getting correct handlers """
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        event = 'iot_dev_state_change'
        handler_name = '_handle_state_change'
        result = mqtt_gateway._get_message_handler(event=event)
        self.assertEqual(result.__name__, handler_name)

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_get_message_handler_unknown_event(self, mock_mqtt_client):
        """ Testing getting correct handlers """
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)
        event = 'not_known_event'
        handler_name = '_unknown_event'
        result = mqtt_gateway._get_message_handler(event=event)
        self.assertEqual(result.__name__, handler_name)

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
    def test_on_message_correct_state_changed(self, mock_mqtt_client):
        """ Testing handling on message """
        mock_mqtt_client.return_value = None
        mqtt_gateway = MqttGateway(queue=self.test_queue, thread_event=self.default_event)

        topic = 'iot/test_topic'
        data = {'device_id': 'dev_001', 'event_type': 'iot_dev_state_change', 'state': True}
        json_data = dumps(data)
        emtpy_queue(queue=self.test_queue)
        mqtt_gateway.on_message(topic=topic, payload=json_data)

        iot_traffic_event = self.test_queue.get()
        self.assertEqual(iot_traffic_event['event'], 'iot_traffic')
        self.assertEqual(iot_traffic_event['message']['source'], 'MqttGateway')
        self.assertEqual(iot_traffic_event['message']['topic'], topic)
        self.assertEqual(iot_traffic_event['message']['payload'], json_data)

        state_changed_event = self.test_queue.get()
        self.assertEqual(state_changed_event['event'], 'device_state_changed')
        self.assertEqual(state_changed_event['message']['device_id'], data.get('device_id'))
        self.assertEqual(state_changed_event['message']['event_type'], data.get('event_type'))
        self.assertEqual(state_changed_event['message']['state'], data.get('state'))

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
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

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
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

    @mock.patch("src.iot_gateway.mqtt_client.MqttClient")
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
