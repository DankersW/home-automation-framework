from unittest import TestCase, mock

from home_automation_framework.iot_gateway.iot_message import IotMessage


class TestIotMessage(TestCase):
    def test_class_attributes(self):
        attributes = ['event', 'device_id', 'payload']
        for attribute in attributes:
            self.assertTrue(hasattr(IotMessage, attribute))

    def test_class_attributes_init_value(self):
        msg = IotMessage
        attributes = ['event', 'device_id', 'payload']
        for attribute in attributes:
            self.assertIsNone(getattr(msg, attribute))

    def test_is_valid(self):
        msg = IotMessage()

        mock_attr_event = mock.PropertyMock(return_value='data123')
        mock_attr_device_id = mock.PropertyMock(return_value='data123')
        mock_attr_payload = mock.PropertyMock(return_value={'data': 'test'})
        type(msg).event = mock_attr_event
        type(msg).device_id = mock_attr_device_id
        type(msg).payload = mock_attr_payload

        self.assertTrue(msg.is_valid())

    def test_is_valid_all_attr_not_set(self):
        msg = IotMessage()

        mock_attr_event = mock.PropertyMock(return_value=None)
        mock_attr_device_id = mock.PropertyMock(return_value=None)
        mock_attr_payload = mock.PropertyMock(return_value=None)
        type(msg).event = mock_attr_event
        type(msg).device_id = mock_attr_device_id
        type(msg).payload = mock_attr_payload

        self.assertFalse(msg.is_valid())

    def test_is_valid_one_attr_not_set(self):
        msg = IotMessage()

        mock_attr_event = mock.PropertyMock(return_value='data123')
        mock_attr_device_id = mock.PropertyMock(return_value=None)
        mock_attr_payload = mock.PropertyMock(return_value={'data': 'test'})
        type(msg).event = mock_attr_event
        type(msg).device_id = mock_attr_device_id
        type(msg).payload = mock_attr_payload

        self.assertFalse(msg.is_valid())

