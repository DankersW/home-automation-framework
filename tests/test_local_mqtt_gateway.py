import unittest

from src.iot_gateway import local_mqtt_gateway


class TestIdFromTopic(unittest.TestCase):
    index_type = 'device_id'

    def test_correct_topics(self):
        topic_list = ["iot/devices/device-001/state", "iot/devices/d1/state", "iot/devices/FA124/state",
                      "iot/devices/randomName/state", "iot/devices/1/state"]
        truth_list = ["device-001", "d1", "FA124", "randomName", "1"]
        for i in range(len(topic_list)):
            test_result = local_mqtt_gateway.get_item_from_topic(topic_list[i], self.index_type)
            self.assertEqual(test_result, truth_list[i])

    def test_not_a_topic(self):
        topic = "iot"
        truth = None
        test_result = local_mqtt_gateway.get_item_from_topic(topic, self.index_type)
        self.assertEqual(test_result, truth)

    def test_no_iot_topic(self):
        topic = "somethingElse/device-001/state"
        truth = None
        test_result = local_mqtt_gateway.get_item_from_topic(topic, self.index_type)
        self.assertEqual(test_result, truth)

    def test_wrong_structure(self):
        topic = "iot/devices/very/wrong/state"
        truth = None
        test_result = local_mqtt_gateway.get_item_from_topic(topic, self.index_type)
        self.assertEqual(test_result, truth)


class TestEventFromTopic(unittest.TestCase):
    index_type = 'event'

    def test_correct_topics(self):
        topic_list = ["iot/devices/device-001/state", "iot/devices/d1/state", "iot/devices/FA14/attach",
                      "iot/devices/randomName/state", "iot/devices/1/attach"]
        truth_list = ["state", "state", "attach", "state", "attach"]
        for i in range(len(topic_list)):
            test_result = local_mqtt_gateway.get_item_from_topic(topic_list[i], self.index_type)
            self.assertEqual(test_result, truth_list[i])


if __name__ == '__main__':
    TestEventFromTopic()
    TestIdFromTopic()