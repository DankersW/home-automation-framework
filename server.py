from src.iot_gateway.iot_gateway import IotGateway


class HomeServer:
    def __init__(self):
        # start listing for connected devices
        iot_gateway = IotGateway(path_cert_dir='keys/')


if __name__ == '__main__':
    home_server = HomeServer()
