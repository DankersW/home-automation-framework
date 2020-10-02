from os import path, remove
from pathlib import Path
import unittest
import yaml

from src.lib.configuration_parser import ConfigurationParser


class TestConfigurationParser(unittest.TestCase):
    conf_parser = ConfigurationParser()

    def test_get_path_to_conf_file(self):
        file_path = self.conf_parser.get_path_to_conf_file()
        if path.isfile(file_path):
            assert True
        else:
            assert False

    """
    def test_yml_to_dict_mock_conf_file(self):
        test_content = {'a': 123, 'b': 456}
        filename = 'test.yaml'
        yml_path = Path.cwd().joinpath(filename)
        with open(yml_path, 'w') as file:
            yaml.dump(test_content, file)
        result = self.conf_parser.yml_to_dict(file_path=yml_path)
        assert result == test_content
        remove(yml_path)
    """
