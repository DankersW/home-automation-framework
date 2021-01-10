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
        message = {'device_id': 'device_001', 'event_type': 'iot_dev_state_change', 'stat': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertTrue(result)

    def test_is_valid_mqtt_message_device_id_missing(self):
        message = {'device_': 'device_001', 'event_type': 'iot_dev_state_change', 'stat': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertFalse(result)

    def test_is_valid_mqtt_message_event_type_missing(self):
        message = {'device_id': 'device_001', 'event_t': 'iot_dev_state_change', 'stat': True}
        result = MqttGateway._is_valid_mqtt_message(msg=message)
        self.assertFalse(result)
