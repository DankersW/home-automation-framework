import datetime
import ssl
import time
import threading
from dataclasses import dataclass
import jwt

import paho.mqtt.client as mqtt

from src.logging.logging import Logging, LogLevels



@dataclass
class MqttGatewayConfiguration:
    project_id: str = "dankers"
    registry_id: str = "home_automation_light_switches"
    gateway_id: str = "home_automation_light_switches_gateway"
    private_key_file: str = "rsa_light_switch_private.pem"
    algorithm: str = "RS256"
    cloud_region: str = "europe-west1"
    ca_certs: str = "roots.pem"
    mqtt_bridge_hostname: str = "mqtt.googleapis.com"
    mqtt_bridge_port: int = 8883


ONE_MILLISECOND_SECONDS = 0.001


def create_jwt(project_id, private_key_file, algorithm):
    """Create a JWT (https://jwt.io) to establish an MQTT connection."""
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return f'{rc} - {mqtt.error_string(rc)}'


class GBridge(threading.Thread):
    mqtt_client = None
    g_bridge_connected = False

    attached_devices = []
    pending_messages = []
    pending_subscribed_topics = []

    received_messages_queue = []

    def __init__(self, path_cert_dir=None):
        threading.Thread.__init__(self)
        self.log = Logging(owner=__file__, log_mode='terminal', min_log_lvl=LogLevels.debug)
        gateway_configuration = MqttGatewayConfiguration()
        if path_cert_dir is not None:
            gateway_configuration.private_key_file = path_cert_dir + gateway_configuration.private_key_file
            gateway_configuration.ca_certs = path_cert_dir + gateway_configuration.ca_certs
        self.gateway_id = gateway_configuration.gateway_id
        self.connect_to_iot_core_broker(gateway_configuration)

    def __del__(self):
        self.detach_all_devices()
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def run(self):
        self.mqtt_client.loop_start()
        self.wait_for_connection(5)
        while self.g_bridge_connected:
            time.sleep(ONE_MILLISECOND_SECONDS)

    def connect_to_iot_core_broker(self, conf):
        # Create the MQTT client and connect to Cloud IoT.
        gateway_id = f'projects/{conf.project_id}/locations/{conf.cloud_region}/registries/' \
                     f'{conf.registry_id}/devices/{conf.gateway_id}'
        self.mqtt_client = mqtt.Client(gateway_id)
        jwt_pwd = create_jwt(conf.project_id, conf.private_key_file, conf.algorithm)
        self.mqtt_client.username_pw_set(username='unused', password=jwt_pwd)
        self.mqtt_client.tls_set(ca_certs=conf.ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.connect(conf.mqtt_bridge_hostname, conf.mqtt_bridge_port)

    def wait_for_connection(self, timeout):
        total_time = 0
        while not self.g_bridge_connected and total_time < timeout:
            time.sleep(1)
            total_time += 1
        if not self.g_bridge_connected:
            self.log.critical('Could not connect to Iot Core MQTT bridge')
            raise RuntimeError()

    def on_connect(self, _unused_client, _unused_userdata, _unused_flags, rc):
        self.log.success(f'Connected to GCP IoT core MQTT Broker with connection Result: {error_str(rc)}')
        self.g_bridge_connected = True
        self.subscribe_to_topics(self.gateway_id, True)
        if self.attached_devices:  # Not empty list, Previously already had connected devices
            self.log.warning('Re-connect occurred! Re-attaching all connected devices.')

    def subscribe_to_topics(self, dev_id, gateway):
        config_topic = f'/devices/{dev_id}/config'
        command_topic = f'/devices/{dev_id}/commands/#'
        subscriptions = [{'topic': config_topic, 'qos': 1}, {'topic': command_topic, 'qos': 1}]
        if gateway:
            gateway_error_topic = f'/devices/{dev_id}/errors'
            subscriptions.append({'topic': gateway_error_topic, 'qos': 0})

        for subscription in subscriptions:
            self.subscribe(subscription.get('topic'), subscription.get('qos'))

    def subscribe(self, topic, qos):
        _, mid = self.mqtt_client.subscribe(topic, qos)
        self.pending_subscribed_topics.append(mid)
        while topic in self.pending_subscribed_topics:
            time.sleep(0.01)
        self.log.debug(f'Successfully subscribed to topic {topic!r} with Qos {qos!r}.')

    def on_disconnect(self, _unused_client, _unused_userdata, rc):
        self.log.warning(f'Disconnected: {error_str(rc)!r}')
        self.g_bridge_connected = False

    def on_publish(self, _unused_client, _unused_userdata, mid):
        self.log.debug(f'ACK received for message {mid!r}')
        if mid in self.pending_messages:
            self.pending_messages.remove(mid)

    def on_subscribe(self, _unused_client, _unused_userdata, mid, granted_qos):
        if granted_qos[0] == 128:
            self.log.error(f'Subscription result: {granted_qos[0]!r} - Subscription failed')
        else:
            if mid in self.pending_subscribed_topics:
                self.pending_subscribed_topics.remove(mid)

    def on_message(self, _unused_client, _unused_userdata, message):
        payload = message.payload.decode('utf-8')
        self.log.info(f'Received message {payload!r} on topic {message.topic!r}.')
        if not payload:
            return

        # todo: fix this so that is better
        if message.topic.split('/')[3] == "commands":
            device_id = GBridge.get_id_from_topic(message.topic)
            message = [device_id, payload]
            self.received_messages_queue.append(message)

    def attach_device(self, device_id):
        self.log.debug(f'Attaching device {device_id!r}.')
        attach_topic = f'/devices/{device_id}/attach'
        if device_id not in self.attached_devices:
            self.attached_devices.append(device_id)
        self.publish(attach_topic, "")  # Message content is empty because gateway auth-method=ASSOCIATION_ONLY
        self.subscribe_to_topics(device_id, False)

    def detach_device(self, device_id):
        self.log.warning(f'Detaching device {device_id!r}.')
        detach_topic = f'/devices/{device_id}/detach'
        if device_id in self.attached_devices:
            self.attached_devices.remove(device_id)
        self.publish(detach_topic, "")  # Message content is empty because gateway auth-method=ASSOCIATION_ONLY

    def detach_all_devices(self):
        self.log.info(f'Detaching all devices. Currently all connected devices: {self.attached_devices}.')
        for device in self.attached_devices[:]:
            self.detach_device(device)
        while self.attached_devices:  # Make sure all devices have been detached
            time.sleep(0.01)

    def publish(self, topic, payload):
        message_info = self.mqtt_client.publish(topic, payload, qos=1)
        self.pending_messages.append(message_info.mid)
        self.log.info(f'Publishing payload: {payload!r} on Topic {topic!r} with mid {message_info.mid!r}.')
        while message_info.mid in self.pending_messages:  # Waiting for message ACK to arrive
            time.sleep(0.01)

    def send_data(self, device_id, event_type, payload):
        if event_type == "telemetry":
            topic = f'/devices/{device_id}/events'
        elif event_type == "state":
            topic = f'/devices/{device_id}/state'
        else:
            self.log.error(f'Unknown event type {event_type}.')
            return
        self.publish(topic, payload)

    def get_last_message(self):
        message_queue = None
        if len(self.received_messages_queue) > 0:
            message_queue = self.received_messages_queue.pop(0)
        return message_queue

    @staticmethod
    def get_id_from_topic(topic):
        index_device_id = 2
        dir_tree = topic.split('/')
        if len(dir_tree) != 4 or dir_tree[1] != "devices":
            return None
        return dir_tree[index_device_id]

    def reattach_devices(self):
        for device in self.attached_devices:
            self.log.info(f'Re-attaching device {device}.')
            self.attach_device(device)


# Quick Tests
def attach_detach_with_2_devices():
    g_bridge = GBridge(path_cert_dir='../../keys/')
    g_bridge.start()
    device_list = ["light_switch_001", "light_switch_002"]

    g_bridge.attach_device(device_list[0])
    g_bridge.attach_device(device_list[1])

    g_bridge.detach_device(device_list[0])
    g_bridge.attach_device(device_list[1])

    time.sleep(2)
    g_bridge.__del__()
    del g_bridge


def keep_running_for_messages():
    g_bridge = GBridge(path_cert_dir='../../keys/')
    g_bridge.start()
    device_list = ["light_switch_001", "light_switch_002"]
    g_bridge.attach_device(device_list[0])

    for _ in range(30):
        message = g_bridge.get_last_message()
        if message is not None:
            print(f"received message queue: {message}")
        time.sleep(1)

    g_bridge.__del__()
    del g_bridge


def send_data():
    g_bridge = GBridge(path_cert_dir='../../keys/')
    g_bridge.start()
    device_list = ["light_switch_001", "light_switch_002"]
    g_bridge.attach_device(device_list[0])
    g_bridge.attach_device(device_list[1])

    g_bridge.send_data(device_list[0], "state", "{\"test\": 123}")
    g_bridge.send_data(device_list[1], "telemetry", "{\"test\": 123}")
    g_bridge.send_data(device_list[0], "telemetry", "{\"test\": 123}")
    g_bridge.send_data(device_list[1], "state", "{\"test\": 123}")
    g_bridge.send_data(device_list[0], "state", "{\"test\": 14}")

    time.sleep(10)
    g_bridge.__del__()
    del g_bridge


def send_message_and_wait():
    g_bridge = GBridge(path_cert_dir='../../keys/')
    g_bridge.start()
    device_list = ["light_switch_001"]
    g_bridge.attach_device(device_list[0])

    time.sleep(5)
    g_bridge.send_data(device_list[0], "state", "{\"light_state\": 1}")
    time.sleep(20)
    g_bridge.send_data(device_list[0], "state", "{\"light_state\": 4}")

    time.sleep(10)
    g_bridge.__del__()
    del g_bridge


if __name__ == '__main__':
    send_message_and_wait()
