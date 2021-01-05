from unittest import TestCase, mock
from queue import Queue
from threading import Event

from src.iot_gateway.mqtt_gateway import MqttGateway


class TestMqttGateway(TestCase):
    """
    @mock.patch.object(MqttGateway, '_get_broker_address')
    def test_connect_mqtt_client_random_address(self, mock_broker_address):
        mock_broker_address.return_value = '200.0.0.0'
        t_queue = Queue(10)
        thread_ready_event = Event()
        mqtt_gateway = MqttGateway(queue=t_queue, thread_event=thread_ready_event)
        self.assertFalse(mqtt_gateway.running)

    @mock.patch.object(MqttGateway, '_get_broker_address')
    def test_connect_mqtt_client_no_running_broker(self, mock_broker_address):
        mock_broker_address.return_value = '127.0.0.1'
        t_queue = Queue(10)
        thread_ready_event = Event()
        mqtt_gateway = MqttGateway(queue=t_queue, thread_event=thread_ready_event)
        self.assertFalse(mqtt_gateway.running)

    @mock.patch.object(MqttGateway, '_get_broker_address')
    def test_connect_mqtt_client_online_broker_connect(self, mock_broker_address):
        mock_broker_address.return_value = 'broker.hivemq.com'
        t_queue = Queue(10)
        thread_ready_event = Event()
        mqtt_gateway = MqttGateway(queue=t_queue, thread_event=thread_ready_event)
        thread_ready_event.wait()
        self.assertTrue(mqtt_gateway.running)
    """

