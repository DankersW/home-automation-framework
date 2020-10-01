import unittest

from src.iot_gateway.iot_gateway import IotGateway


class TestDecodeJson(unittest.TestCase):
    def test_wrong_key(self):
        json_string = '{"wrong_key":  True}'
        key = "good_key"
        required_value = None
        test_result = IotGateway.decode_json(json_string, key)
        self.assertEqual(test_result, required_value)

    def test_no_key(self):
        json_string = "{}"
        key = "a_key"
        required_value = None
        test_result = IotGateway.decode_json(json_string, key)
        self.assertEqual(test_result, required_value)

    def test_not_json_string(self):
        json_string = '{"forgot_the_closing_quotes: 10}'
        key = "forgot_the_closing_quotes"
        required_value = None
        test_result = IotGateway.decode_json(json_string, key)
        self.assertEqual(test_result, required_value)

    def test_correct_key_value_pairs(self):
        json_strings = ['{"key_a": 10}', '{"key_b": "hello"}', '{"key_c": true}', '{"key_d": 1, "key_e": 2}',
                        '{"key_f": 14.15}']
        keys = ['key_a', 'key_b', 'key_c', 'key_e']
        required_values = [10, 'hello', True, 2, 14.15]
        for json_string, key, required_value in zip(json_strings, keys, required_values):
            test_result = IotGateway.decode_json(json_string, key)
            self.assertEqual(test_result, required_value)

    def test_no_value(self):
        json_string = '{"key_a": }'
        key = "key_a"
        required_value = None
        test_result = IotGateway.decode_json(json_string, key)
        self.assertEqual(test_result, required_value)


if __name__ == '__main__':
    unittest.main()
