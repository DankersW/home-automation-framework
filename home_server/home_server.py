from src.iot_gateway import IotGateway


class HomeServer:
    def __init__(self):
        # start listing for connected devices
        iot_gateway = IotGateway()


if __name__ == '__main__':
    home_server = HomeServer()
