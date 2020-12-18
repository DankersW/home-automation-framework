from threading import Thread
from queue import Queue
from pathlib import Path
from time import time, sleep
import subprocess

from src.logging.logging import Logging


class HealthMonitor(Thread):
    running = True
    update_time_sec = 30

    def __init__(self, queue: Queue) -> None:
        Thread.__init__(self)
        self.observer_publish_queue = queue
        self.observer_notify_queue = Queue(maxsize=100)
        self.log = Logging(owner=__file__, config=True)

    def __del__(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            start_time = time()

            host_data = self._fetch_host_data()
            item = {'event': 'host_health', 'message': host_data}
            self.observer_publish_queue.put(item)

            sleep_time = self.update_time_sec - ((time() - start_time) % self.update_time_sec)
            sleep(sleep_time)

    def notify(self, msg: dict, event: str) -> None:
        pass

    def _fetch_host_data(self) -> dict:
        data = {
            'temperature': self.poll_system_temp(),
            'cpu_load': self.poll_cpu_load()
        }
        return data

    def poll_system_temp(self) -> float:
        temp_file = self._get_temperature_file()
        try:
            with open(temp_file) as file:
                return float(file.readline()) / 1000
        except FileNotFoundError:
            self.log.critical(f'Temperature file {temp_file!r} does not exist')
        return 0

    @staticmethod
    def _get_temperature_file() -> Path:
        return Path('/sys/class/thermal/thermal_zone0/temp')

    def poll_cpu_load(self) -> float:
        cpu_command = ["cat", "/proc/stat"]
        try:
            process_result = subprocess.Popen(cpu_command, stdout=subprocess.PIPE)
            proc_stat, _ = process_result.communicate()
            cpu_data = proc_stat.decode('utf-8').split('\n')[0].split()[1:-1]
            cpu_data = [int(field) for field in cpu_data]
            cpu_usage = ((cpu_data[0] + cpu_data[2]) * 100 / (cpu_data[0] + cpu_data[2] + cpu_data[3]))
            return round(cpu_usage, 3)
        except FileNotFoundError:
            self.log.critical(f'Command {" ".join(cpu_command)!r} was not found on the system')
        return 0


if __name__ == '__main__':
    test_queue = Queue(10)
    hm = HealthMonitor(test_queue)
    hm.start()
