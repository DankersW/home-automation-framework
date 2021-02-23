from unittest import TestCase
from mock import PropertyMock
from datetime import datetime

from home_automation_framework.logging.persistent_logging import DbLogging


class TestLogging(TestCase):
    db_logging = DbLogging()

    def test_generate_document_name(self):
        base_name = 'test_log'
        mock_conf_property = PropertyMock(return_value={'logging_tests': {'log_collection_name': base_name}})
        type(self.db_logging).config = mock_conf_property

        time = datetime.now()
        dt = time.strftime('%Y%m%d%H%M')
        result = self.db_logging.generate_collection_name(time)
        assert result == f'{base_name}_{dt}'

    def test_already_logging_not_logging(self):
        collection_list = ['logs_202010220842', 'logs_202010251025', 'logs_202010251026']
        result, _ = self.db_logging.already_logging(collection_list)
        assert not result

    def test_already_logging_already_logging(self):
        logging_collection = f'logs_{datetime.now().strftime("%Y%m%d%H%M")}'
        collection_list = ['logs_202010220842', 'logs_202010251025', 'logs_202010251026', logging_collection]
        result, name = self.db_logging.already_logging(collection_list)
        assert result
        assert name == logging_collection
