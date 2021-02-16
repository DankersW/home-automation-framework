class IotMessage:
    event: str = ""
    mqtt_topic: str = ""

    def __init__(self, message: dict) -> None:
        # todo: if json --> do something
        # todo: serialize the data
        # todo: parse message
        pass

    def __dict__(self) -> dict:
        pass

    def is_valid(self) -> bool:
        pass
