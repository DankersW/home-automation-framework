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


class HealthMonitor(Thread):
    running = True
    update_time_sec = 600
    subscribed_event = []

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
        while self.running:
            """
            queue_item = self._observer_notify_queue.get()
            print(queue_item)
            item = {'event': 'host_health', 'message': "test"}
            self._observer_publish_queue.put(item)
            """
            pass

    def notify(self, msg: dict, event: str) -> None:
        self._observer_notify_queue.put(item=msg)


if __name__ == '__main__':
    test_queue = Queue(10)
    t_event = Event()
    hm = HealthMonitor(test_queue, thread_event=t_event)
    hm.start()

