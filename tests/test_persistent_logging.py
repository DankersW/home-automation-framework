from unittest import TestCase
from mock import PropertyMock

from src.logging.persistent_logging import DbLogging


class TestLogging(TestCase):
    db_logging = DbLogging('test')

    def test_generate_document_name(self):
        mock_conf_property = PropertyMock({'logging': {'log_document': 'test_log'}})
        type(a).var_a = mock_var_a_property

        self.db_logging.generate_document_name()


        # mock config file