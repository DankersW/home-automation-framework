# https://www.protechtraining.com/blog/post/tutorial-the-observer-pattern-in-python-879

class GBridgeObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print('{} got message "{}"'.format(self.name, message))


class LocalMqttGatewayObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print('{} got message "{}"'.format(self.name, message))


class DbObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print('{} got message "{}"'.format(self.name, message))


class GenericObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, msg):
        print(f'{self.name}: received event event and message {msg} -- setting incomming message queue')


class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))


class Subject:
    def __init__(self, events):
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, events, observer, callback=None):
        if callback is None:
            callback = getattr(observer, 'notify')
        for event in events:
            self.get_subscribers(event)[observer] = callback

    def unregister(self, event, observer):
        del self.get_subscribers(event)[observer]

    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)


def driver():
    events = ['gcp_comm', 'device_comm']
    iot_observer = Subject(events)

    g_bridge_observer = GenericObserver(name='g_bridge')
    local_mqtt_observer = GenericObserver(name='local_mqtt')
    db_observer = GenericObserver(name='db_handler')

    iot_observer.register(observer=g_bridge_observer, events=['gcp_comm'])
    iot_observer.register(observer=local_mqtt_observer, events=['device_comm'])
    iot_observer.register(observer=db_observer, events=['device_comm', 'gcp_comm'])

    iot_observer.dispatch('device_comm', 'data for devices')
    iot_observer.dispatch('gcp_comm', 'gcp data')


if __name__ == '__main__':
    driver()
