from threading import Thread, Event, Timer, Lock
from queue import Queue
from typing import Callable, Union, List
from time import time, sleep

from home_automation_framework.framework.observer_message import ObserverMessage
from home_automation_framework.logging.logging import Logging
from home_automation_framework.utils.configuration_parser import ConfigurationParser


class DeviceManager(Thread):
    running = True
    subscribed_event = ['digital_twin']
    remote_digital_twin = []
    device_status_map = {}
    poll_timer = None
    new_devices = False

    def __init__(self, queue: Queue, thread_event: Event) -> None:
        Thread.__init__(self)
        self._observer_publish_queue = queue
        self._thread_ready = thread_event
        self._observer_notify_queue = Queue(maxsize=100)
        self.log = Logging(owner=__file__, config=True)

        self.config = ConfigurationParser().get_config()
        self.poll_interval = self.config["device_manager"]["poll_interval"]
        self.device_map_lock = Lock()

    def __del__(self) -> None:
        self.running = False

    def notify(self, event: str, msg: ObserverMessage) -> None:
        self.log.debug(f"Received event {event} on notify")
        self._observer_notify_queue.put(item=msg)

    def run(self) -> None:
        self._thread_ready.set()
        self._fetch_digital_twin()
        self._start_timer(interval=self.poll_interval, callback=self._timer_callback)

        while self.running:
            queue_msg = self._observer_notify_queue.get()
            if queue_msg.event == "digital_twin":
                self._handle_digital_twin_event(msg=queue_msg)

        self.poll_timer.cancel()

    def _fetch_digital_twin(self):
        msg = ObserverMessage(event="digital_twin", data={}, subject="fetch_digital_twin")
        self._observer_publish_queue.put(msg)

    def _start_timer(self, interval: int, callback: Callable) -> None:
        self.poll_timer = Timer(interval=interval, function=callback)
        self.poll_timer.start()

    def _handle_digital_twin_event(self, msg: ObserverMessage):
        if msg.subject == "retrieved_digital_twin":
            self._store_remote_digital_twin(data=msg.data)
        elif msg.subject == "device_status":
            self._store_device_status(data=msg.data)

    def _store_remote_digital_twin(self, data: dict):
        self.remote_digital_twin = data
        self.log.success("Received remote digital twin")
        self.log.debug(f"Remote digital twin: {self.remote_digital_twin}")

    def _store_device_status(self, data: dict):
        device_id = data.get("device_id", None)
        status = data.get("active", None)
        self.log.debug(f"Received device status {status} from {device_id}")
        if device_id and status:
            self.device_status_map[device_id] = status

    def _timer_callback(self):
        self.log.debug("Starting device status polling stage")
        self.device_status_map = self._generate_device_map_from_remote_twin()

        self._publish_device_status_poll()
        wait_period = self.config["device_manager"]["wait_period"]
        self._wait_for_status_messages(wait_period=wait_period)

        digital_twin = self._create_digital_twin_from_device_status()
        if digital_twin:
            self._publish_digital_twin(twin=digital_twin)

        if self.new_devices:
            self._fetch_digital_twin()
            self.new_devices = False

        self._start_timer(interval=self.poll_interval, callback=self._timer_callback)

    def _generate_device_map_from_remote_twin(self) -> dict:
        device_map = {}
        for twin_item in self.remote_digital_twin:
            device_name = twin_item["device_name"]
            device_map[device_name] = False
        return device_map

    def _publish_device_status_poll(self):
        msg = ObserverMessage(event="digital_twin", data={}, subject="poll_devices")
        self._observer_publish_queue.put(msg)

    def _wait_for_status_messages(self, wait_period: Union[int, float]) -> None:
        self.log.debug(f"Starting waiting period of {wait_period} seconds")
        start_time = time()
        while self.running and (time() - start_time < wait_period):
            sleep(0.01)
        self.log.debug("Waiting period over")

    def _create_digital_twin_from_device_status(self) -> Union[None, List[dict]]:
        if not self.device_status_map and not self.remote_digital_twin:
            self.log.debug("No digital twin created since remote and local twin are empty")
            return None

        with self.device_map_lock:
            device_status_map = self.device_status_map.copy()

        digital_twin = []
        for remote_item in self.remote_digital_twin:
            device_id = remote_item["device_name"]
            helper = remote_item
            if device_id in device_status_map:
                helper["active"] = device_status_map[device_id]
                del device_status_map[device_id]
            digital_twin.append(helper)

        for new_device in device_status_map:
            new_item = {"device_name": new_device, "active": True, "location": None,
                        "technology": None, "battery_level": None}
            digital_twin.append(new_item)
            self.new_devices = True

        return digital_twin

    def _publish_digital_twin(self, twin: Union[list, dict]) -> None:
        msg = ObserverMessage(event="digital_twin", data=twin, subject="save_digital_twin")
        self._observer_publish_queue.put(msg)
