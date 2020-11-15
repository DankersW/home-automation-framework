import time
from src.iot_gateway.g_bridge import GBridge


# Quick Tests
def attach_detach_with_2_devices():
    g_bridge = GBridge()
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
    g_bridge = GBridge()
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
    g_bridge = GBridge()
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
    g_bridge = GBridge()
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
