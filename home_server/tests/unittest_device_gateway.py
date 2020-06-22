import unittest

from home_server.src import device_gateway


class TestIdFromTopic(unittest.TestCase):
    index_type = 'device_id'

    def test_correct_topics(self):
        topic_list = ["iot/device-001/state", "iot/d1/state", "iot/FA124/state", "iot/randomName/state", "iot/1/state"]
        truth_list = ["device-001", "d1", "FA124", "randomName", "1"]
        for i in range(len(topic_list)):
            test_result = device_gateway.get_item_from_topic(topic_list[i], self.index_type)
            self.assertEqual(test_result, truth_list[i])

    def test_not_a_topic(self):
        topic = "iot"
        truth = None
        test_result = device_gateway.get_item_from_topic(topic, self.index_type)
        self.assertEqual(test_result, truth)

    def test_no_iot_topic(self):
        topic = "somethingElse/device-001/state"
        truth = None
        test_result = device_gateway.get_item_from_topic(topic, self.index_type)
        self.assertEqual(test_result, truth)

    def test_wrong_structure(self):
        topic = "iot/very/wrong/state"
        truth = None
        test_result = device_gateway.get_item_from_topic(topic, self.index_type)
        self.assertEqual(test_result, truth)


class TestEventFromTopic(unittest.TestCase):
    index_type = 'event'

    def test_correct_topics(self):
        topic_list = ["iot/device-001/state", "iot/d1/state", "iot/FA14/attach", "iot/randomName/state", "iot/1/attach"]
        truth_list = ["state", "state", "attach", "state", "attach"]
        for i in range(len(topic_list)):
            test_result = device_gateway.get_item_from_topic(topic_list[i], self.index_type)
            self.assertEqual(test_result, truth_list[i])


if __name__ == '__main__':
    TestEventFromTopic()
    TestIdFromTopic()