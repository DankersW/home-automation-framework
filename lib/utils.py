from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_keys_dir() -> Path:
    return Path(get_project_root(), 'keys')
