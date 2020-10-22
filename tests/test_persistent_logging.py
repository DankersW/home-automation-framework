from unittest import TestCase
from mock import PropertyMock
from datetime import datetime

from src.logging.persistent_logging import DbLogging


class TestLogging(TestCase):
    db_logging = DbLogging()

    def test_generate_document_name(self):
        base_name = 'test_log'
        mock_conf_property = PropertyMock(return_value={'logging': {'log_collection': base_name}})
        type(self.db_logging).config = mock_conf_property

        time = datetime.now()
        dt = time.strftime('%Y%m%d%H%M')
        result = self.db_logging.generate_collection_name(time)
        assert result == f'{base_name}_{dt}'
