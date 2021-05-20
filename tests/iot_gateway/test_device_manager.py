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

    def test_create_digital_twin_from_device_status_both_remote_and_local_none(self):
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.device_status_map = {}
        device_manager.remote_digital_twin = []
        result = device_manager._create_digital_twin_from_device_status()
        self.assertIsNone(result)

    def test_create_digital_twin_from_device_status_unit_still_active(self):
        remote_twin = [{"_id": "ObjectId('6089b77907384800073936a6')", "device_name": 'test_device',
                        "active": True, "location": 'on-desk', "technology": 'WI-FI', "battery_level": 'USB-power'},
                       {"_id": "ObjectId('6089b77907384800073936a6')", "device_name": 'test_device_17',
                        "active": True, "location": 'on-desk', "technology": 'WI-FI', "battery_level": 'USB-power'}
                       ]
        correct_dt = remote_twin
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.device_status_map = {"test_device": True, "test_device_17": True}
        device_manager.remote_digital_twin = remote_twin
        result = device_manager._create_digital_twin_from_device_status()
        self.assertListEqual(correct_dt, result)

    def test_create_digital_twin_from_device_status_one_offline(self):
        remote_twin = [{"device_name": 'test_device', "active": True}, {"device_name": 'test_device_1', "active": True}]
        correct_dt = [{"device_name": 'test_device', "active": True}, {"device_name": 'test_device_1', "active": False}]
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.device_status_map = {"test_device": True, "test_device_1": False}
        device_manager.remote_digital_twin = remote_twin
        result = device_manager._create_digital_twin_from_device_status()
        self.assertListEqual(correct_dt, result)

    def test_create_digital_twin_from_device_status_new_device(self):
        correct_dt = [{'device_name': 'new_device', 'status': True, 'location': None, 'technology': None,
                       'battery_level': None}]
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.device_status_map = {"new_device": True}
        device_manager.remote_digital_twin = []
        result = device_manager._create_digital_twin_from_device_status()
        self.assertListEqual(result, correct_dt)

    def test_create_digital_twin_from_device_status_one_old_one_new_device(self):
        remote_twin = {"_id": "ObjectId('6089b77907384800073936a6')", "device_name": 'test_device', "active": True,
                       "location": 'on-desk', "technology": 'WI-FI', "battery_level": 'USB-power'}
        correct_dt = [remote_twin,
                      {'device_name': 'new_device', 'status': True, 'location': None,
                       'technology': None, 'battery_level': None}]
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.device_status_map = {"new_device": True}
        device_manager.remote_digital_twin = [remote_twin]
        result = device_manager._create_digital_twin_from_device_status()
        self.assertListEqual(result, correct_dt)

    def test_generate_device_map_from_remote_twin_emtpy_twin(self):
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.remote_digital_twin = []
        device_map = device_manager._generate_device_map_from_remote_twin()
        self.assertDictEqual(device_map, {})

    def test_generate_device_map_from_remote_twin_correct_twin_structure(self):
        correct_map = {"test_device": False}
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.remote_digital_twin = [{"_id": "ObjectId('6089b77907384800073936a6')",
                                               "device_name": 'test_device', "active": True, "location": 'on-desk',
                                               "technology": 'WI-FI', "battery_level": 'USB-power'}]
        device_map = device_manager._generate_device_map_from_remote_twin()
        self.assertDictEqual(device_map, correct_map)

    def test_generate_device_map_from_remote_twin_multi_items(self):
        correct_map = {"test_device": False, "abc": False}
        device_manager = DeviceManager(queue=self.test_queue, thread_event=self.default_event)
        device_manager.remote_digital_twin = [{"device_name": 'test_device'}, {"device_name": "abc"}]
        device_map = device_manager._generate_device_map_from_remote_twin()
        self.assertDictEqual(device_map, correct_map)
