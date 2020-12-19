from os import remove
from pathlib import Path
from queue import Queue


def create_test_file_with_data(file: Path, data: str) -> None:
    with open(file, 'w') as file:
        file.write(data)


def delete_file(file: Path) -> None:
    if file.exists():
        remove(file)


def emtpy_queue(queue: Queue) -> None:
    while not queue.empty():
        queue.get()
