# https://www.protechtraining.com/blog/post/tutorial-the-observer-pattern-in-python-879

class GBridgeObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, msg, event):
        print(f'{self.name}: {event} - {msg}')


class LocalMqttGatewayObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, msg, event):
        print(f'{self.name}: {event} - {msg}')


class DbObserver:
    def __init__(self, name):
        self.name = name

    def notify(self, msg, event):
        print(f'{self.name}: {event} - {msg}')


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
            callback(message, event)


class IotSubject:
    observers = []

    def __init__(self):
        events = ['gcp_comm', 'device_comm']
        self.subject = Subject(events)
        self.init_observers()
        self.attach_observers()

    def init_observers(self):
        self.observers.append({'observer': GBridgeObserver(name='g_bridge'), 'events': ['gcp_comm']})
        self.observers.append({'observer': LocalMqttGatewayObserver(name='local_mqtt'), 'events': ['device_comm']})
        self.observers.append({'observer': DbObserver(name='db_handler'), 'events': ['gcp_comm', 'device_comm']})

    def attach_observers(self):
        for observer in self.observers:
            self.subject.register(**observer)

    def run(self):
        # todo: poll all overserver queues
        # todo: dispatch all gatered events
        test_events = [{'event': 'gcp_comm', 'message': 'random data'},
                       {'event': 'device_comm', 'message': 'local random data'},
                       {'event': 'device_comm', 'message': 'someting data'},
                       {'event': 'device_comm', 'message': 'another v data'}]
        self.subject.dispatch('gcp_comm', 'gcp data')
        self.subject.dispatch('device_comm', 'data for devices')

        self.notify_observers(events=test_events)
        
    def notify_observers(self, events):
        for event in events:
            self.subject.dispatch(**event)


if __name__ == '__main__':
    iot_subject = IotSubject()
    iot_subject.run()
