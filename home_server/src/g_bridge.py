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
    message_type: str = "event"


def create_jwt(project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class MqttGcpDevice(object):
    def __init__(self, device_id):
        self.args = MqttBridgeConfiguration()
        self.connected = False
        self.device_id = device_id
        self.client = self.create_client()
        self.setup_connection()

    def __del__(self):
        self.client.disconnect()
        self.client.loop_stop()

    def create_client(self):
        client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(self.args.project_id,
                                                                               self.args.cloud_region,
                                                                               self.args.registry_id,
                                                                               self.device_id)
        client = mqtt.Client(client_id)
        jwt_pwd = create_jwt(self.args.project_id, self.args.private_key_file, self.args.algorithm)
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
            raise RuntimeError('Could not connect to MQTT bridge.')

    def subscribe_to_topics(self):
        mqtt_config_topic = '/devices/{}/config'.format(self.device_id)
        self.client.subscribe(mqtt_config_topic)

    def publish_telemetry_event(self, payload):
        mqtt_telemetry_topic = '/devices/{}/events'.format(self.device_id)
        print('Publishing payload: {} - Topic: {}'.format(payload, mqtt_telemetry_topic))
        self.client.publish(mqtt_telemetry_topic, payload, qos=1)

    def publish_state_event(self, payload):
        mqtt_state_topic = '/devices/{}/state'.format(self.device_id)
        print('Publishing payload: {} - Topic: {}'.format(payload, mqtt_state_topic))
        self.client.publish(mqtt_state_topic, payload, qos=1)

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        print('Published message acked.')

    def on_subscribe(self, unused_client, unused_userdata, unused_mid, granted_qos):
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        payload = message.payload.decode('utf-8')
        if not payload:
            return
        data = json.loads(payload)
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(payload, message.topic, str(message.qos)))


class GBridge:
    def __init__(self, device_list):
        device_id = device_list
        self.device = MqttGcpDevice(device_id)
        self.main()

    def __del__(self):
        pass

    def main(self):
        self.device.publish_telemetry_event("temp: 11")
        self.device.publish_telemetry_event("temp: 12")
        self.device.publish_telemetry_event("temp: 13")
        time.sleep(15)


def main():
    GBridge()


if __name__ == '__main__':
    main()
