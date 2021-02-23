from unittest import TestCase, mock

from home_automation_framework.iot_gateway.iot_message import IotMessage


class TestIotMessage(TestCase):
    test_topic = 'iot/devices/dev_001/state'
    test_payload = {'state': True}

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
        msg = IotMessage(mqtt_topic=self.test_topic, data=self.test_payload)

        mock_attr_event = mock.PropertyMock(return_value='data123')
        mock_attr_device_id = mock.PropertyMock(return_value='data123')
        mock_attr_payload = mock.PropertyMock(return_value={'data': 'test'})
        type(msg).event = mock_attr_event
        type(msg).device_id = mock_attr_device_id
        type(msg).payload = mock_attr_payload

        self.assertTrue(msg.is_valid())

    def test_is_valid_all_attr_not_set(self):
        msg = IotMessage(mqtt_topic=self.test_topic, data=self.test_payload)

        mock_attr_event = mock.PropertyMock(return_value=None)
        mock_attr_device_id = mock.PropertyMock(return_value=None)
        mock_attr_payload = mock.PropertyMock(return_value=None)
        type(msg).event = mock_attr_event
        type(msg).device_id = mock_attr_device_id
        type(msg).payload = mock_attr_payload

        self.assertFalse(msg.is_valid())

    def test_is_valid_one_attr_not_set(self):
        msg = IotMessage(mqtt_topic=self.test_topic, data=self.test_payload)

        mock_attr_event = mock.PropertyMock(return_value='data123')
        mock_attr_device_id = mock.PropertyMock(return_value=None)
        mock_attr_payload = mock.PropertyMock(return_value={'data': 'test'})
        type(msg).event = mock_attr_event
        type(msg).device_id = mock_attr_device_id
        type(msg).payload = mock_attr_payload

        self.assertFalse(msg.is_valid())

    @mock.patch.object(IotMessage, '_parse_data')
    @mock.patch.object(IotMessage, '_get_device_id_from_topic')
    @mock.patch.object(IotMessage, '_get_event_from_topic')
    def test_init(self, mock_get_event, mock_get_dev_id, mock_parse_data):
        mock_get_event.return_value = 'state'
        mock_get_dev_id.return_value = 'dev001'
        mock_parse_data.return_value = {'state': True}
        msg = IotMessage(mqtt_topic=self.test_topic, data=self.test_payload)
        self.assertEqual(msg.event, 'state')
        self.assertEqual(msg.device_id, 'dev001')
        self.assertDictEqual(msg.payload, {'state': True})

    def test__destruct_topic_event(self):
        event = IotMessage._destruct_topic(topic=self.test_topic, item_index=3)
        self.assertEqual(event, 'state')

    def test__destruct_topic_device_id(self):
        dev_id = IotMessage._destruct_topic(topic=self.test_topic, item_index=2)
        self.assertEqual(dev_id, 'dev_001')

    def test__destruct_topic_bad_topics(self):
        for topic in ['iot/devices/', 'iot/device/d/state', 'iot_/devices/test/state', 'devices/test/state']:
            destructed_topic = IotMessage._destruct_topic(topic=topic, item_index=2)
            self.assertIsNone(destructed_topic)
