from typing import Union


class ObserverMessage:
    source: str = None
    destination: str = None
    data: Union[str, dict] = None
    event: str = None
    subject: str = None

    def __init__(self) -> None:
        pass

