from threading import Thread
from queue import Queue
from pathlib import Path
from typing import List

from src.logging.logging import Logging


class HealthMonitor(Thread):
    running = False

    def __init__(self, queue: Queue) -> None:
        Thread.__init__(self)
        self.observer_publish_queue = queue
        self.observer_notify_queue = Queue(maxsize=100)
        self.log = Logging(owner=__file__, config=True)

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            item = self.observer_notify_queue.get()

        self.poll_system_temp()

    def notify(self, msg: dict, event: str) -> None:
        pass

    def poll_system_temp(self) -> List[str]:
        temp_file = self.get_temperature_file()
        try:
            with open(temp_file) as file:
                return file.readlines()
        except FileNotFoundError:
            self.log.critical(f'Temperature file {temp_file!r} does not exist')
        return []

    @staticmethod
    def get_temperature_file() -> Path:
        return Path('/sys/class/thermal/thermal_zone0/temp')


if __name__ == '__main__':
    test_queue = Queue(10)
    hm = HealthMonitor(test_queue)
