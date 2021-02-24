from unittest import TestCase

from home_automation_framework.framework.framework import IotSubject


class TestIotSubject(TestCase):
    def test_get_matching_object(self):
        print(IotSubject._get_matching_object(component_name='gcp').__name__)

        components = {
            'gcp': 'GBridge',
            'mqtt_gateway': 'MqttGateway',
            'db': 'DbHandler',
            'host_monitor': 'HealthMonitor'
        }
        for component in components.keys():
            object_name = IotSubject._get_matching_object(component_name=component).__name__
            self.assertEqual(object_name, components[component])
