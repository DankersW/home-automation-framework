from os import path
import unittest


from src.lib.configuration_parser import ConfigurationParser


class TestConfigurationParser(unittest.TestCase):
    conf_parser = ConfigurationParser()

    def test_get_path_to_conf_file(self):
        file_path = self.conf_parser.get_path_to_conf_file()
        print(file_path)
        if path.isfile(path.realpath(file_path)):
            assert True
        assert False
