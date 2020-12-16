from threading import Thread
from queue import Queue


class HealthMonitor(Thread):
    running = True

    def __init__(self, queue: Queue) -> None:
        Thread.__init__(self)
        self.observer_publish_queue = queue
        self.observer_notify_queue = Queue(maxsize=100)

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            item = self.observer_notify_queue.get()

    def notify(self, msg: dict, event: str) -> None:
        self.observer_notify_queue.put({'event': event, 'msg': msg})
