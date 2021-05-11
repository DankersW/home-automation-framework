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

import time

from home_automation_framework.framework.observer_message import ObserverMessage
from home_automation_framework.logging.logging import Logging


class DeviceManager(Thread):
    running = True
    update_time_sec = 600
    subscribed_event = ['digital_twin']
    remote_digital_twin = []
    poll_timer = None

    # todo: cleanup function order

    def __init__(self, queue: Queue, thread_event: Event) -> None:
        Thread.__init__(self)
        self._observer_publish_queue = queue
        self._thread_ready = thread_event
        self._observer_notify_queue = Queue(maxsize=100)
        self.log = Logging(owner=__file__, config=True)

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        self._thread_ready.set()
        self._fetch_digital_twin()

        self._start_timer(callback=self._timer_callback)

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
        device_id = data.get("device_id", "Unknown")
        self.log.debug(f"Reveived device status from {device_id}")
        # todo: store all status in a set (device_id, status)

    def _timer_callback(self):

        self._start_timer(callback=self._timer_callback)
        # todo: clean status list
        # todo: send out cmd to mqtt gateway to receive status
        # todo: wait for a certain time
        # todo: map the remote digital twin with the status set and create digital_twin dict
        # todo: publish new digital twin to the cloud
        # todo: restart timer if needed

    def _start_timer(self, callback: Callable) -> None:
        self.poll_timer = Timer(interval=5, function=callback)
        self.poll_timer.start()


if __name__ == '__main__':
    test_queue = Queue(10)
    t_event = Event()
    dm = DeviceManager(test_queue, thread_event=t_event)
    dm.start()

