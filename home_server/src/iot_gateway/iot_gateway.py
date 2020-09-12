import time
import json

from home_server.src.iot_gateway.device_gateway import DeviceGateway
from home_server.src.iot_gateway.g_bridge import GBridge


class IotGateway:
    running = True

    def __init__(self, path_cert_dir=None):
        self.device_gateway = DeviceGateway()
        self.device_gateway.start()

        self.g_bridge = GBridge(path_cert_dir)
        self.g_bridge.start()

        self.run()

    def __del__(self):
        del self.g_bridge
        self.device_gateway.join()

    def run(self):

        while self.running:
            self.device_to_cloud_communication()
            self.cloud_to_device_communication()
            time.sleep(0.001)

    def device_to_cloud_communication(self):
        # Take oldest message from device_gateway gueue and poss it to the Gbridge
        message = self.device_gateway.get_last_message()
        if message is not None:
            device = message[0]
            event = message[2]
            if event == 'attach':
                self.g_bridge.attach_device(device)
            elif event == 'state':
                print('message: \'{}\''.format(message[1]))
                data = '{"light_state": ' + message[1] + '}'
                self.g_bridge.send_data(device, event, data)

    def cloud_to_device_communication(self):
        message = self.g_bridge.get_last_message()
        if message is not None:
            json_key = 'light_state'
            json_string = message[1]
            device = message[0]
            data = decode_json(json_string, json_key)
            if data is not None:
                self.device_gateway.publish_control_message(device, data)


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
    iotGateway = IotGateway(path_cert_dir='../certificates/')
