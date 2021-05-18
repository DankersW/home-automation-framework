# todo: define digital_twin document (status, location, technology, batterie level)

"""
Flow:
    init
        download digital twin from db
        create local digital-twin struct with status zero-d
        create device_status_poll_timer with callback

    device_status_poll_timer_cb
        send out status_request msg to all units
        wait for x minutes to getter responses
        plublish digital-twin status to db
        zero twin struct
        start timer

    start
        listen for messages, on message update digital twin wih status to active

"""

from threading import Thread, Event, Timer
from queue import Queue
from typing import Callable
from time import time, sleep
from typing import Union

from home_automation_framework.framework.observer_message import ObserverMessage
from home_automation_framework.logging.logging import Logging
from home_automation_framework.utils.configuration_parser import ConfigurationParser


class DeviceManager(Thread):
    running = True
    update_time_sec = 600
    subscribed_event = ['digital_twin']
    remote_digital_twin = []
    device_status_map = {}
    poll_timer = None

    # todo: cleanup function order

    def __init__(self, queue: Queue, thread_event: Event) -> None:
        Thread.__init__(self)
        self._observer_publish_queue = queue
        self._thread_ready = thread_event
        self._observer_notify_queue = Queue(maxsize=100)
        self.log = Logging(owner=__file__, config=True)

        self.config = ConfigurationParser().get_config()
        self.poll_interval = self.config["device_manager"]["poll_interval"]
        self.wait_period = self.config["device_manager"]["wait_period"]

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        self._thread_ready.set()
        self._fetch_digital_twin()

        self._start_timer(interval=self.poll_interval, callback=self._timer_callback)

        while self.running:
            queue_msg = self._observer_notify_queue.get()
            if queue_msg.event == "digital_twin":
                self._handle_digital_twin_event(msg=queue_msg)

        self.poll_timer.cancel()

    def notify(self, event: str, msg: ObserverMessage) -> None:
        self._observer_notify_queue.put(item=msg)

    def _fetch_digital_twin(self):
        msg = ObserverMessage(event="digital_twin", data={}, subject="fetch_digital_twin")
        self._observer_publish_queue.put(msg)

    def _handle_digital_twin_event(self, msg: ObserverMessage):
        if msg.subject == "retrieved_digital_twin":
            self._store_remote_digital_twin(data=msg.data)
        elif msg.subject == "device_status":
            self._store_device_status(data=msg.data)

    def _store_remote_digital_twin(self, data: dict):
        self.remote_digital_twin = data
        self.log.success(f"Received remote digital twin")
        self.log.debug(f"Remote digital twin: {self.remote_digital_twin}")

    def _store_device_status(self, data: dict):
        device_id = data.get("device_id", None)
        status = data.get("status", None)
        self.log.debug(f"Reveived device status {status} from {device_id}")
        if device_id and status:
            self.device_status_map[device_id] = status

    def _timer_callback(self):
        self.log.debug("Starting device status polling stage")
        self.device_status_map = {}

        # TODO
        self._publish_device_status_poll()

        self._wait_for_status_messages(wait_period=self.wait_period)

        # TODO
        self._update_digital_twin_with_device_status()

        # TODO
        self._publish_digital_twin()

        if self.running:
            self._start_timer(interval=self.poll_interval, callback=self._timer_callback)

    def _wait_for_status_messages(self, wait_period: Union[int, float]) -> None:
        self.log.debug(f"Starting waiting period of {wait_period} seconds")
        start_time = time()
        while self.running and (time() - start_time < wait_period):
            sleep(0.01)
        print("done")

    def _start_timer(self, interval: int, callback: Callable) -> None:
        self.poll_timer = Timer(interval=interval, function=callback)
        self.poll_timer.start()

    def _publish_device_status_poll(self):
        pass

    def _publish_digital_twin(self):
        pass

    def _update_digital_twin_with_device_status(self):
        pass


if __name__ == '__main__':
    test_queue = Queue(10)
    t_event = Event()
    dm = DeviceManager(test_queue, thread_event=t_event)
    dm.start()

