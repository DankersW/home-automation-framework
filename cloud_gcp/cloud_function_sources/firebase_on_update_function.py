from google.cloud import pubsub_v1


def firestore_on_update_to_devices_pubsub(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    name = event['value']['name']
    state = event['value']['fields']['state']['integerValue']
    device_id = get_device_id_from_name(name)
    payload = '{"state": ' + state + '}'
    if device_id is None:
        return

    #send_data_to_device(device_id, payload)


def get_device_id_from_name(name):
    index_device_id = 6
    dir_tree = name.split('/')
    valid_name = len(dir_tree) is 7 and 'light_switch' in dir_tree[index_device_id]
    if valid_name:
        return dir_tree[index_device_id]
    return None


def send_data_to_device(device_id, payload):
    project_id = 'dankers'
    topic_id = '/devices/{}/commands'.format(device_id)
    payload = payload.encode("utf-8")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, data=payload)
    print(future.result())


if __name__ == '__main__':
    event = {'oldValue': {'createTime': '2020-05-25T11:18:18.595997Z', 'fields': {'online': {'booleanValue': False}, 'state': {'integerValue': '0'}}, 'name': 'projects/dankers/databases/(default)/documents/devices/light_switch_001', 'updateTime': '2020-06-06T03:09:15.009407Z'}, 'updateMask': {'fieldPaths': ['state']}, 'value': {'createTime': '2020-05-25T11:18:18.595997Z', 'fields': {'online': {'booleanValue': False}, 'state': {'integerValue': '1'}}, 'name': 'projects/dankers/databases/(default)/documents/devices/light_switch_001', 'updateTime': '2020-06-06T03:09:15.009407Z'}}
    context = None
    firestore_on_update_to_devices_pubsub(event, context)
