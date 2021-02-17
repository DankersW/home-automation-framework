from typing import Union
from json import loads

from home_automation_framework.utils.utils import is_json


class IotMessage:
    event: str = None
    device_id: str = None
    payload: dict = None

    def __init__(self, mqtt_topic: str = None, data: Union[str, dict] = None) -> None:
        self.event = self._get_event_from_topic(topic=mqtt_topic)
        self.device_id = self._get_device_id_from_topic(topic=mqtt_topic)
        self.payload = self._parse_data(data=data)

    def _get_event_from_topic(self, topic: str) -> Union[str, None]:
        pass

    def _get_device_id_from_topic(self, topic: str) -> Union[str, None]:
        pass

    def _parse_data(self, data: Union[str, dict]) -> Union[dict, None]:
        if isinstance(data, dict):
            return data
        elif is_json(data):
            return loads(data)
        return None

    def is_valid(self) -> bool:
        for attr in ['event', 'device_id', 'payload']:
            if getattr(self, attr) is None:
                return False
        return True


if __name__ == '__main__':
    msg = IotMessage('None')
    print(msg.is_valid())
