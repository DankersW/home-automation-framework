from src.device_gateway import DeviceGateway

class HomeServer:
    def __init__(self):
        # start listing for connected devices
        device_gateway = DeviceGateway()


if __name__ == '__main__':
    home_server = HomeServer()
