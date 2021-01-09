from unittest import TestCase, mock
from paho.mqtt import client

from src.iot_gateway.mqtt_client import MqttClient, IllegalArgumentError


class TestMqttClient(TestCase):
    def mock_callback(self, **kwargs):
        pass

    def test_valid_arguments_correct(self):
        """ Test valid arguments """
        test_config = {'broker': '127.0.0.1'}
        callbacks = [self.mock_callback, self.mock_callback]
        self.assertTrue(MqttClient.valid_arguments(config=test_config, callbacks=callbacks))

    def test_valid_arguments_invalid_config(self):
        """ Test bad config """
        test_config = {'wrong': '127.0.0.1'}
        callbacks = [self.mock_callback, self.mock_callback]
        try:
            MqttClient.valid_arguments(config=test_config, callbacks=callbacks)
        except IllegalArgumentError:
            self.assertTrue(True)

    def test_valid_arguments_1_function_not_callable(self):
        """ Test bad callbacks """
        test_config = {'broker': '127.0.0.1'}
        callbacks = [self.mock_callback, 'not_callable']
        try:
            MqttClient.valid_arguments(config=test_config, callbacks=callbacks)
        except IllegalArgumentError:
            self.assertTrue(True)

    def test_valid_arguments_all_functions_not_callable(self):
        """ Test bad callbacks """
        test_config = {'broker': '127.0.0.1'}
        callbacks = ['not_callable', 'not_callable']
        try:
            MqttClient.valid_arguments(config=test_config, callbacks=callbacks)
        except IllegalArgumentError:
            self.assertTrue(True)

    def test_valid_arguments_all_invalid(self):
        """ Test bad callbacks """
        test_config = {'not_valid': '127.0.0.1'}
        callbacks = ['not_callable', 'not_callable']
        try:
            MqttClient.valid_arguments(config=test_config, callbacks=callbacks)
        except IllegalArgumentError:
            self.assertTrue(True)

    @mock.patch.object(client, 'Client')
    def test_connect_success(self, mock_client):
        """ Test connecting, mocked paho part """
        conf = {'broker': '127.0.0.1'}
        mock_client.return_value = MockClient
        _client = MqttClient(config=conf, connect_callback=self.mock_callback, message_callback=self.mock_callback)
        self.assertTrue(_client.connect())

    @mock.patch.object(client, 'Client')
    def test_connect_timeout_error(self, mock_client):
        """ Test timeout error, mocked paho part """
        conf = {'broker': '127.0.0.1'}
        mock_client.return_value = MockClientTimeoutError
        _client = MqttClient(config=conf, connect_callback=self.mock_callback, message_callback=self.mock_callback)
        self.assertFalse(_client.connect())

    @mock.patch.object(client, 'Client')
    def test_connect_refused_error(self, mock_client):
        """ Test connection refused error, mocked paho part """
        conf = {'broker': '127.0.0.1'}
        mock_client.return_value = MockClientConnectionRefused
        _client = MqttClient(config=conf, connect_callback=self.mock_callback, message_callback=self.mock_callback)
        self.assertFalse(_client.connect())

    def test_publish_success(self):
        """ Testing publishing, mocking the actual publish"""
        conf = {'broker': '127.0.0.1'}
        _client = MqttClient(config=conf, connect_callback=self.mock_callback, message_callback=self.mock_callback)
        mock_mqtt_client = mock.PropertyMock(return_value=MockClientPublishSuccess)
        type(_client)._mqtt_client = mock_mqtt_client
        self.assertTrue(_client.publish("test", {'a': 12}))

    def test_publish_fail(self):
        """ Testing publishing, mocking the actual publish"""
        conf = {'broker': '127.0.0.1'}
        _client = MqttClient(config=conf, connect_callback=self.mock_callback, message_callback=self.mock_callback)
        mock_mqtt_client = mock.PropertyMock(return_value=MockClientPublishFail)
        type(_client)._mqtt_client = mock_mqtt_client
        self.assertFalse(_client.publish("test", {'a': 12}))


class MockClient:
    @staticmethod
    def connect(**_kwargs):
        pass

    @staticmethod
    def loop_start(**_kwargs):
        pass


class MockClientConnectionRefused(MockClient):
    @staticmethod
    def loop_start(**kwargs):
        raise ConnectionRefusedError


class MockClientTimeoutError(MockClient):
    @staticmethod
    def loop_start(**kwargs):
        raise TimeoutError


class MockMessageInfo:
    rc = 0


class MockClientPublishSuccess(MockClient):
    @staticmethod
    def publish(**_kwargs):
        msg_success = MockMessageInfo()
        msg_success.rc = 0
        return msg_success


class MockClientPublishFail(MockClient):
    @staticmethod
    def publish(**_kwargs):
        msg_fail = MockMessageInfo()
        msg_fail.rc = 1
        return msg_fail
