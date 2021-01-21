from unittest import TestCase
from json import dumps

from home_automation_framework.utils.utils import is_json


class TestUtils(TestCase):
    def test_is_json_correct(self):
        data = {'abc': 123}
        json_data = dumps(data)
        self.assertTrue(is_json(text=json_data))

    def test_is_json_no_json_string(self):
        data = 'no_json'
        self.assertFalse(is_json(text=data))
