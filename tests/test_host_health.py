from unittest import TestCase
from unittest.mock import patch
from queue import Queue
from pathlib import Path

import mock

from src.host_health.health_monitor import HealthMonitor
from tests.helper_functions import create_test_file_with_data, delete_file


class TestHostHealth(TestCase):
    test_queue = Queue(10)
    health_monitor = HealthMonitor(test_queue)

    @patch.object(HealthMonitor, '_get_temperature_file')
    def test_poll_system_temp_no_file_exist(self, mock_file_path):
        """ Test to get the temperature but temperature file does not exist """
        mock_file_path.return_value = Path('test/123')
        self.assertEqual(self.health_monitor.poll_system_temp(), 0)

    @patch.object(HealthMonitor, '_get_temperature_file')
    def test_poll_system_temp_correct(self, mock_file_path):
        """ Test to get the temperature and compare what has been published matches return """
        file_path = Path(Path().cwd(), 'test')
        mock_temp = 12345
        create_test_file_with_data(file=file_path, data=str(mock_temp))
        mock_file_path.return_value = file_path
        self.assertEqual(self.health_monitor.poll_system_temp(), mock_temp)
        delete_file(file=file_path)

    @mock.patch('subprocess.Popen')
    def test_poll_cpu_load_correct(self, mock_popen):
        process_mock = mock.Mock()
        test_data = b'cpu  1697429 0 1156929 16854817 0 172800 0 0 0 0'
        attrs = {'communicate.return_value': (test_data, 'error')}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock
        self.assertEqual(self.health_monitor.poll_cpu_load(), 14.482)
