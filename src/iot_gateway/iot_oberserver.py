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
    def __init__(self, name, observer):
        pass

    def notify(self):
        pass


class Subject:  # Publisher
    def __init__(self, events):
        # maps event names to subscribers
        # str -> dict
        self.events = {event: dict()
                       for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback=None):
        if callback == None:
            callback = getattr(who, 'update')
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)


def driver():
    pub = Subject(['lunch', 'dinner'])
    bob = Subscriber('Bob')
    alice = Subscriber('Alice')
    john = Subscriber('John')

    pub.register("lunch", bob)
    pub.register("dinner", alice)
    pub.register("lunch", john)
    pub.register("dinner", john)

    pub.dispatch("lunch", "It's lunchtime!")
    pub.dispatch("dinner", "Dinner is served")

    for event in ['lunch', 'dinner']:
        print(pub.get_subscribers(event))


if __name__ == '__main__':
    driver()
