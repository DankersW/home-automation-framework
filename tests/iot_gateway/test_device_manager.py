import time
from unittest import TestCase, mock
from queue import Queue
from threading import Event
from json import dumps

from home_automation_framework.iot_gateway.device_manager import DeviceManager
from tests.helper_functions import emtpy_queue


class TestDeviceManager(TestCase):
    test_queue = Queue(10)
    default_event = Event()

    def test_fetch_digital_twin_triggered_on_start(self):
        emtpy_queue(queue=self.test_queue)
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.running = False
        device_manager.start()
        send_msg = self.test_queue.get()
        truth = {'event': 'digital_twin', 'message': {'action': 'fetch_digital_twin'}}
        self.assertDictEqual(send_msg, truth)

    def test_store_remote_digital_twin(self):
        emtpy_queue(queue=self.test_queue)
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.start()
        moch_dt = ["abc"]
        notify_msg = {"action": "retrieved_digital_twin", "data": moch_dt}
        device_manager.notify(msg=notify_msg, event="")
        time.sleep(0.5)
        self.assertEqual(device_manager.remote_digital_twin, moch_dt)
        device_manager.running = False
        device_manager.notify(msg={"stop": True}, event="")
