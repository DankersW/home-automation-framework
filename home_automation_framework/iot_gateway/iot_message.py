from typing import Union
from json import loads

from home_automation_framework.utils.utils import is_json


class IotMessage:
    event: str = None
    device_id: str = None
    payload: dict = None

    def __init__(self, mqtt_topic: str, data: Union[str, dict]) -> None:
        self.event = self._get_event_from_topic(topic=mqtt_topic)
        self.device_id = self._get_device_id_from_topic(topic=mqtt_topic)
        self.payload = self._parse_data(data=data)

    def _get_event_from_topic(self, topic: str) -> Union[str, None]:
        return self._destruct_topic(topic=topic, item_index=3)

    def _get_device_id_from_topic(self, topic: str) -> Union[str, None]:
        return self._destruct_topic(topic=topic, item_index=2)

    @staticmethod
    def _destruct_topic(topic: str, item_index: int) -> Union[str, None]:
        topic_structure = topic.split('/')
        valid_topic = len(topic_structure) == 4 and topic_structure[0] == "iot" and topic_structure[1] == "devices"
        if not valid_topic:
            return None
        return topic_structure[item_index]

    @staticmethod
    def _parse_data(data: Union[str, dict]) -> Union[dict, None]:
        parsed_data = None
        if isinstance(data, dict):
            parsed_data = data
        elif is_json(data):
            parsed_data = loads(data)
        return parsed_data

    def is_valid(self) -> bool:
        for attr in ['event', 'device_id', 'payload']:
            if getattr(self, attr) is None:
                return False
        return True
