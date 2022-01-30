import datetime
import ssl
import time
import threading
from dataclasses import dataclass
from pathlib import Path
from queue import Queue

import jwt
import paho.mqtt.client as mqtt

from home_automation_framework.logging.logging import Logging, LogLevels
from home_automation_framework.utils.utils import get_keys_dir


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
    with open(private_key_file, 'r', encoding="utf8") as f:
        private_key = f.read()
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return f'{rc} - {mqtt.error_string(rc)}'


class GBridge(threading.Thread):
    subscribed_event = ['device_state_changed']

    mqtt_client = None
    g_bridge_connected = False

    attached_devices = []
    pending_messages = []
    pending_subscribed_topics = []

    def __init__(self, queue, thread_event: threading.Event):
        threading.Thread.__init__(self)
        self.log = Logging(owner=__file__, log_mode='terminal', min_log_lvl=LogLevels.debug)
        gateway_configuration = MqttGatewayConfiguration()

        self.observer_notify_queue = Queue(maxsize=100)
        self.observer_publish_queue = queue
        self._thread_ready = thread_event

        keys_dir = get_keys_dir()
        gateway_configuration.private_key_file = Path(keys_dir, gateway_configuration.private_key_file)
        gateway_configuration.ca_certs = Path(keys_dir, gateway_configuration.ca_certs)
        self.gateway_id = gateway_configuration.gateway_id
        self.connect_to_iot_core_broker(gateway_configuration)

    def __del__(self):
        self.detach_all_devices()
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def run(self):
        self.mqtt_client.loop_start()
        self.wait_for_connection(5)
        self._thread_ready.set()
        while self.g_bridge_connected:
            queue_item = self.observer_notify_queue.get()
            self.send_data(msg=queue_item)
            time.sleep(ONE_MILLISECOND_SECONDS)

    def notify(self, msg, _) -> None:
        self.observer_notify_queue.put(item=msg)

    @staticmethod
    def poll_events():
        return []

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
            queue_message = {'device_id': device_id, 'event_type': 'command', 'payload': payload}
            item = {'event': 'gcp_state_changed', 'message': queue_message}
            self.observer_publish_queue.put(item)

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

    def send_data(self, msg):
        device_id = msg.get('device_id')
        event_type = msg.get('event_type')
        payload = msg.get('payload')

        if device_id not in self.attached_devices:
            self.attach_device(device_id=device_id)

        if event_type == 'telemetry':
            topic = f'/devices/{device_id}/events'
        elif event_type == 'state':
            topic = f'/devices/{device_id}/state'
        else:
            self.log.error(f'Unknown event type {event_type}.')
            return
        self.publish(topic, payload)

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
