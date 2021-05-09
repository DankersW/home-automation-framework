from typing import Union
from inspect import stack


class ObserverMessage:
    def __init__(self, event: str, data: Union[str, dict, list], subject: str = None, destination: str = None) -> None:
        self.event = event
        self.data = data
        self.subject = subject
        self.destination = destination
        self.source = stack()[1][0].f_locals.get("self", None).__class__.__name__

    def __str__(self):
        attrs = vars(self)
        return f"ObserverMessage {attrs}"
