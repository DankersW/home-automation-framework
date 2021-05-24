from os import path, remove
from pathlib import Path
from unittest import TestCase
import yaml


from home_automation_framework.utils.configuration_parser import ConfigurationParser
from tests.helper_functions import isinstance_namedtuple


class TestConfigurationParser(TestCase):
    conf_parser = ConfigurationParser()

    def test_get_path_to_conf_file(self):
        file_path = self.conf_parser._get_path_to_conf_file()
        is_file = path.isfile(file_path)
        self.assertTrue(is_file)

    def test_yml_to_dict_mock_conf_file(self):
        test_content = {'a': 123, 'b': 456}
        filename = 'test.yaml'
        yml_path = Path.cwd().joinpath(filename)
        with open(yml_path, 'w') as file:
            yaml.dump(test_content, file)
        result = self.conf_parser._yml_to_dict(file_path=yml_path)
        self.assertDictEqual(result, test_content)
        remove(yml_path)

    def test_as_named_tuple(self):
        config = self.conf_parser.as_named_tuple()
        is_named_tuple = isinstance_namedtuple(config)
        self.assertTrue(is_named_tuple)
