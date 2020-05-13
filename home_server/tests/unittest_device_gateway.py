import unittest

from home_server.src import device_gateway


class TestIdFromTopic(unittest.TestCase):
    def test_correct_topics(self):
        topic_list = ["iot/device-001/state", "iot/d1/state", "iot/FA124/state", "iot/randomName/state", "iot/1/state"]
        truth_list = ["device-001", "d1", "FA124", "randomName", "1"]
        for i in range(len(topic_list)):
            test_result = device_gateway.get_id_from_topic(topic_list[i])
            self.assertEqual(test_result, truth_list[i])

    def test_not_a_topic(self):
        topic = "iot"
        truth = None
        test_result = device_gateway.get_id_from_topic(topic)
        self.assertEqual(test_result, truth)

    def test_no_iot_topic(self):
        topic = "somethingElse/device-001/state"
        truth = None
        test_result = device_gateway.get_id_from_topic(topic)
        self.assertEqual(test_result, truth)

    def test_wrong_structure(self):
        topic = "iot/very/wrong/state"
        truth = None
        test_result = device_gateway.get_id_from_topic(topic)
        self.assertEqual(test_result, truth)


if __name__ == '__main__':
    unittest.main()
