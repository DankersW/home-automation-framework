from pathlib import Path
from json import loads


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_keys_dir() -> Path:
    return Path(get_project_root(), 'keys')


def is_json(text: str) -> bool:
    """ Validates if a string is a JSON object """
    try:
        loads(text)
    except ValueError:
        return False
    return True
