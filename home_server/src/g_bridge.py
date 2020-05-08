import datetime
import json
import ssl
import time
import jwt
import paho.mqtt.client as mqtt
from dataclasses import dataclass


@dataclass
class MqttBridgeConfiguration:
    project_id: str = "dankers"
    registry_id: str = "home_automation_light_switches"
    private_key_file: str = "../certificates/rsa_light_switch_private.pem"
    algorithm: str = "RS256"
    cloud_region: str = "europe-west1"
    ca_certs: str = "../certificates/roots.pem"
    mqtt_bridge_hostname: str = "mqtt.googleapis.com"
    mqtt_bridge_port: int = 8883


def create_jwt(device_id, project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    current_time = datetime.datetime.now()
    print("{} - {} | Creating JWT from private key file using {} algorithm.".format(current_time, device_id, algorithm))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return '{} - {}'.format(rc, mqtt.error_string(rc))


class GBridge:
    def __init__(self, device_list):
        self.device_list = device_list
        self.device = []
        for device_id in self.device_list:
            current_time = datetime.datetime.now()
            print("{} - G-Bridge | Creating device {}".format(current_time, device_id))
            self.device.append(MqttGcpDevice(device_id))

    def __del__(self):
        for device_index in range(len(self.device_list)):
            self.device[device_index].disconnect()

    def publish_data(self, device, event, data):
        device_index = self.device_list.index(device) if device in self.device_list else -1
        if device_index > -1:
            self.device[device_index].publish_data(event, data)
        else:
            print("G-Bridge | device does not exist")
            # todo: create the new device

    def receive_data(self, device, data):
        current_time = datetime.datetime.now()
        print("{} - G-Bridge | Received {} from {}.".format(current_time, data, device))


class MqttGcpDevice(GBridge):
    def __init__(self, device_id):
        self.args = MqttBridgeConfiguration()
        self.connected = False
        self.device_id = device_id
        self.client = self.create_client()
        self.setup_connection()

    def __del__(self):
        self.client.disconnect()
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def create_client(self):
        client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(self.args.project_id,
                                                                               self.args.cloud_region,
                                                                               self.args.registry_id,
                                                                               self.device_id)
        client = mqtt.Client(client_id)
        jwt_pwd = create_jwt(self.device_id, self.args.project_id, self.args.private_key_file, self.args.algorithm)
        client.username_pw_set(username='unused', password=jwt_pwd)
        client.tls_set(ca_certs=self.args.ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)
        return client

    def setup_connection(self):
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.connect(self.args.mqtt_bridge_hostname, self.args.mqtt_bridge_port)
        self.client.loop_start()
        self.wait_for_connection(5)

    def wait_for_connection(self, timeout):
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            current_time = datetime.datetime.now()
            raise RuntimeError("{} - {} | Could not connect to MQTT bridge.".format(current_time, self.device_id))

    def subscribe_to_topics(self):
        mqtt_config_topic = '/devices/{}/config'.format(self.device_id)
        self.client.subscribe(mqtt_config_topic)

    def publish_data(self, event, data):
        if event == "telemetry":
            self.publish_telemetry_event(data)
        elif event == "state":
            self.publish_state_event(data)
        else:
            current_time = datetime.datetime.now()
            print("{} - {} | Error: Unknown event type {}.".format(current_time, self.device_id, event))

    def publish_telemetry_event(self, payload):
        mqtt_telemetry_topic = '/devices/{}/events'.format(self.device_id)
        current_time = datetime.datetime.now()
        print("{} - {} | Publishing payload: \"{}\" on Topic: \"{}\".".format(current_time, self.device_id, payload,
                                                                             mqtt_telemetry_topic))
        self.client.publish(mqtt_telemetry_topic, payload, qos=1)

    def publish_state_event(self, payload):
        mqtt_state_topic = '/devices/{}/state'.format(self.device_id)
        current_time = datetime.datetime.now()
        print("{} - {} | Publishing payload: \"{}\" on Topic: \"{}\".".format(current_time, self.device_id, payload,
                                                                             mqtt_state_topic))
        self.client.publish(mqtt_state_topic, payload, qos=1)

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        current_time = datetime.datetime.now()
        print("{} - {} | Connection Result: {}".format(current_time, self.device_id, error_str(rc)))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        current_time = datetime.datetime.now()
        print("{} - {} | Disconnected: {}".format(current_time, self.device_id, error_str(rc)))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        current_time = datetime.datetime.now()
        print("{} - {} | Published message acknowledged.".format(current_time, self.device_id))

    def on_subscribe(self, unused_client, unused_userdata, unused_mid, granted_qos):
        current_time = datetime.datetime.now()
        if granted_qos[0] == 128:
            subscription_result = "{} - Subscription failed".format(granted_qos[0])
        else:
            subscription_result = "{} - Subscribed".format(granted_qos)
        print("{} - {} | Subscription result: {}.".format(current_time, self.device_id, subscription_result))

    def on_message(self, unused_client, unused_userdata, message):
        payload = message.payload.decode('utf-8')
        if not payload:
            return
        data = json.loads(payload)
        current_time = datetime.datetime.now()
        print("{} - {} | Received message \'{}\' on topic \'{}\' with Qos {}.".format(current_time, self.device_id,
                                                                                      payload, message.topic,
                                                                                      str(message.qos)))
        super().receive_data(self.device_id, payload)


if __name__ == '__main__':
    devices = ["light_switch_001", "light_switch_002"]
    gbridge = GBridge(devices)
    gbridge.publish_data(devices[0], "telemetry", "hello! does it work?")
    time.sleep(10)
    del gbridge
