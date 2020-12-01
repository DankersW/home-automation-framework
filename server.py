from src.iot_gateway.iot_oberserver import IotSubject


class HomeServer:
    def __init__(self):
        # start listing for connected devices
        iot_subject = IotSubject()
        iot_subject.run()


if __name__ == '__main__':
    home_server = HomeServer()
