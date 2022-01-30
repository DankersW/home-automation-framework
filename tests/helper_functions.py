from os import remove
from pathlib import Path
from queue import Queue
from collections import namedtuple
from typing import Union, NamedTuple, Any


def create_test_file_with_data(file: Path, data: str) -> None:
    with open(file, 'w', encoding="utf8") as file:
        file.write(data)


def delete_file(file: Path) -> None:
    if file.exists():
        remove(file)


def emtpy_queue(queue: Queue) -> None:
    while not queue.empty():
        queue.get()


def isinstance_namedtuple(obj: Union[bool, str, int, list, dict, tuple, NamedTuple]) -> bool:
    return isinstance(obj, tuple) and hasattr(obj, '_asdict') and hasattr(obj, '_fields')
