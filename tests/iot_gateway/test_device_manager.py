from unittest import TestCase
from queue import Queue
from threading import Event, Thread
from time import time, sleep

from home_automation_framework.iot_gateway.device_manager import DeviceManager
from home_automation_framework.framework.observer_message import ObserverMessage
from tests.helper_functions import emtpy_queue


class TestDeviceManager(TestCase):
    test_queue = Queue(10)
    default_event = Event()

    def test_fetch_digital_twin_triggered_on_start(self):
        emtpy_queue(queue=self.test_queue)
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.running = False
        device_manager.start()
        msg = self.test_queue.get()
        self.assertEqual(msg.event, "digital_twin")
        self.assertEqual(msg.subject, "fetch_digital_twin")

    def test_store_remote_digital_twin(self):
        emtpy_queue(queue=self.test_queue)
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.start()
        moch_dt = ["abc"]
        notify_msg = ObserverMessage(event="digital_twin", subject="retrieved_digital_twin", data=moch_dt)
        device_manager.notify(msg=notify_msg, event="")
        sleep(0.5)
        self.assertEqual(device_manager.remote_digital_twin, moch_dt)
        device_manager.running = False
        device_manager.notify(msg=ObserverMessage(data="", event=""), event="")

    def test_wait_for_status_messages_not_running(self):
        wait_period = 0.5
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.running = False

        start_time = time()
        device_manager._wait_for_status_messages(wait_period=wait_period)
        end_time = time()

        execution_time = end_time - start_time
        self.assertLess(execution_time, wait_period)

    def test_wait_for_status_messages_run(self):
        wait_period = 0.5
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.running = True

        start_time = time()
        device_manager._wait_for_status_messages(wait_period=wait_period)
        end_time = time()

        execution_time = end_time - start_time
        self.assertGreaterEqual(execution_time, wait_period)

    def test_wait_for_status_messages_stop_mid_run(self):
        wait_period = 25
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.running = True

        func_exec_threat = Thread(target=device_manager._wait_for_status_messages, args=(wait_period,))
        start_time = time()
        func_exec_threat.start()
        sleep(1)
        device_manager.running = False
        func_exec_threat.join()
        end_time = time()

        execution_time = end_time - start_time
        self.assertLess(execution_time, wait_period)
