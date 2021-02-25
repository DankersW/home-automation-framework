from unittest import TestCase, mock

from home_automation_framework.framework.framework import IotSubject, Subject
from home_automation_framework.logging.logging import Logging
from home_automation_framework.utils.configuration_parser import ConfigurationParser


class MockObj:
    subscribed_event = ['iot_traffic']

    def __init__(self, queue, thread_event):
        pass

    def start(self):
        pass


class MockObj2Events(MockObj):
    subscribed_event = ['iot_traffic', 'device_sensor_data']


class FakeWait:
    @staticmethod
    def wait():
        pass


class MockLogging:
    @staticmethod
    def success(*k):
        pass


class TestIotSubject(TestCase):
    configuration = {'system_components': {'gcp': False, 'mqtt_gateway': True, 'db': True, 'host_monitor': True}}

    @mock.patch.object(IotSubject, 'start_observer_threats')
    @mock.patch.object(IotSubject, 'attach_observers')
    @mock.patch.object(IotSubject, 'init_observers')
    @mock.patch.object(Subject, '__init__')
    @mock.patch.object(ConfigurationParser, 'get_config')
    @mock.patch.object(Logging, '__init__')
    def init_iot_subject(self, m_logging, m_config_prs, m_subject, m_init, m_attach, m_start_t) -> IotSubject:
        m_logging.return_value = None
        m_config_prs.return_value = self.configuration
        m_subject.return_value = None
        m_init.return_value = None
        m_attach.return_value = None
        m_start_t.return_value = None
        return IotSubject()

    def test_get_matching_object(self):
        components = {
            'gcp': 'GBridge',
            'mqtt_gateway': 'MqttGateway',
            'db': 'DbHandler',
            'host_monitor': 'HealthMonitor'
        }
        for component in components.keys():
            object_name = IotSubject._get_matching_object(component_name=component).__name__
            self.assertEqual(object_name, components[component])

    def test_get_activated_components(self):
        components = ['mqtt_gateway', 'db', 'host_monitor']
        iot_subject = self.init_iot_subject()
        activated_components = iot_subject._get_activated_components()
        self.assertEqual(components, activated_components)

    @mock.patch.object(IotSubject, '_get_matching_object')
    @mock.patch.object(IotSubject, '_get_activated_components')
    def test_init_observers_1obj_1event(self, mock_get_comp, mock_get_obj):
        iot_subject = self.init_iot_subject()
        iot_subject.observers = []
        mock_get_comp.return_value = ['db']
        mock_get_obj.return_value = MockObj
        iot_subject.init_observers()
        observers = iot_subject.observers
        self.assertEqual(len(observers), 1)
        self.assertEqual(observers[0]['obs_object'].__class__.__name__, 'MockObj')
        self.assertEqual(observers[0]['events'], ['iot_traffic'])

    @mock.patch.object(IotSubject, '_get_matching_object')
    @mock.patch.object(IotSubject, '_get_activated_components')
    def test_init_observers_2obj_2event(self, mock_get_comp, mock_get_obj):
        iot_subject = self.init_iot_subject()
        iot_subject.observers = []
        mock_get_comp.return_value = ['db', 'another_one']
        mock_get_obj.return_value = MockObj2Events
        iot_subject.init_observers()
        observers = iot_subject.observers
        self.assertEqual(len(observers), 2)
        for observer in observers:
            self.assertEqual(observer['obs_object'].__class__.__name__, 'MockObj2Events')
            self.assertEqual(observer['events'],  ['iot_traffic', 'device_sensor_data'])

    @mock.patch.object(IotSubject, '_get_matching_object')
    @mock.patch.object(IotSubject, '_get_activated_components')
    def test_start_observer_threats(self, mock_get_comp, mock_get_obj):
        iot_subject = self.init_iot_subject()
        iot_subject.observers = []
        mock_get_comp.return_value = ['db']
        mock_get_obj.return_value = MockObj
        iot_subject.init_observers()
        iot_subject._thread_started_event = FakeWait
        iot_subject.log = MockLogging
        iot_subject.start_observer_threats()
        self.assertTrue(iot_subject.running)
