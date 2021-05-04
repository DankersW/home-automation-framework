# todo: create an event to read from mongodb
# todo: mongo, fetch digital_twin docement
# todo: define digital_twin document (status, location, technology, batterie level)
# todo: setup basic skelethon

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

from threading import Thread, Event
from queue import Queue

from home_automation_framework.logging.logging import Logging


class DeviceManager(Thread):
    running = True
    update_time_sec = 600
    subscribed_event = ['digital_twin']
    remote_digital_twin = []

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
        while self.running:
            queue_item = self._observer_notify_queue.get()
            print(f"tt: {queue_item}")
            if queue_item.get("action") == "retrieved_digital_twin":
                self._store_remote_digital_twin(data=queue_item)

    def notify(self, msg: dict, event: str) -> None:
        self._observer_notify_queue.put(item=msg)

    def _fetch_digital_twin(self):
        item = {'event': 'digital_twin', 'message': {"action": "fetch_digital_twin"}}
        self._observer_publish_queue.put(item)

    def _store_remote_digital_twin(self, data: dict):
        self.log.debug("Fetched data from cloud")
        self.remote_digital_twin = data.get("data")
        self.log.info(f"Remote digitial twin: {self.remote_digital_twin}")


if __name__ == '__main__':
    test_queue = Queue(10)
    t_event = Event()
    dm = DeviceManager(test_queue, thread_event=t_event)
    dm.start()

