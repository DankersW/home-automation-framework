from unittest import TestCase

from home_automation_framework.framework.observer_message import ObserverMessage


class TestObserverMessage(TestCase):
    def test_init(self):
        event_name = "test"
        data = "hello"
        subject = "test 1"
        msg = ObserverMessage(event=event_name, data=data, subject=subject)
        self.assertEqual(msg.event, event_name)
        self.assertEqual(msg.data, data)
        self.assertEqual(msg.subject, subject)
        self.assertEqual(msg.source, self.__class__.__name__)
        self.assertEqual(msg.destination, None)

    def test_to_str(self):
        event_name = "test"
        data = "hello"
        subject = "test 1"
        result = "ObserverMessage {'event': 'test', 'data': 'hello', 'subject': 'test 1', 'destination': None, 'source': 'TestObserverMessage'}"
        msg = ObserverMessage(event=event_name, data=data, subject=subject)
        self.assertEqual(str(msg), result)
