from typing import Union


class IotMessage:
    event: str = None
    device_id: str = None
    payload: dict = None

    def __init__(self, data: Union[str, dict] = None) -> None:
        self._parse_data(data=data)

    def _parse_data(self, data: Union[str, dict]) -> None:
        # todo: if json --> do something
        # todo: serialize the data
        # todo: parse message
        pass

    def is_valid(self) -> bool:
        for attr in ['event', 'device_id', 'payload']:
            if getattr(self, attr) is None:
                return False
        return True


if __name__ == '__main__':
    msg = IotMessage('None')
    print(msg.is_valid())
