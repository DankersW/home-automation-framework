from unittest import TestCase, mock
from queue import Queue
from threading import Event
from json import dumps

from home_automation_framework.iot_gateway.device_manager import DeviceManager
from tests.helper_functions import emtpy_queue


class TestDeviceManager(TestCase):
    def test_a(self):
        self.assertTrue(1)