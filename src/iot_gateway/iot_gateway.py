import time
import json

from src.logging.logging import Logging
from src.iot_gateway.g_bridge import GBridge
from src.iot_gateway.local_mqtt_gateway import LocalMqttGateway
from lib.configuration_parser import ConfigurationParser


class IotGateway:
    running = True

    def __init__(self, path_cert_dir=None):
        self.log = Logging(owner=__file__, config=True)
        self.config = ConfigurationParser().get_config()
        self.gcp = self.config['general']['gcp']
        if self.gcp:
            self.log.info('Starting up G-Bridge')
            self.g_bridge = GBridge(path_cert_dir)
            self.g_bridge.start()

        self.local_mqtt = self.config['general']['local_mqtt_gateway']
        if self.local_mqtt:
            self.log.info('Starting up Local MQTT gateway')
            self.local_mqtt_gateway = LocalMqttGateway()
            self.local_mqtt_gateway.start()

        self.run()

    def __del__(self):
        del self.g_bridge
        self.local_mqtt_gateway.join()

    def run(self):

        while self.running:
            if self.gcp and self.local_mqtt:
                self.device_to_cloud_communication()
                self.cloud_to_device_communication()
                time.sleep(0.001)

    def device_to_cloud_communication(self):
        # Take oldest message from device_gateway gueue and poss it to the Gbridge
        message = self.local_mqtt_gateway.get_last_message()
        if message is not None:
            device = message[0]
            event = message[2]
            if event == 'attach':
                self.g_bridge.attach_device(device)
            elif event == 'state':
                self.log.info(f'message: {message[1]!r}')
                data = '{"light_state": ' + message[1] + '}'
                self.g_bridge.send_data(device, event, data)

    def cloud_to_device_communication(self):
        message = self.g_bridge.get_last_message()
        if message is not None:
            json_key = 'light_state'
            json_string = message[1]
            device = message[0]
            data = self.decode_json(json_string, json_key)
            if data is not None:
                self.local_mqtt_gateway.publish_control_message(device, data)

    @staticmethod
    def decode_json(json_string, key):
        try:
            json_data = json.loads(json_string)
            data = None
            if key in json_data:
                data = json_data[key]
            return data
        except ValueError:
            return None


if __name__ == '__main__':
    iotGateway = IotGateway(path_cert_dir='../../keys/')
