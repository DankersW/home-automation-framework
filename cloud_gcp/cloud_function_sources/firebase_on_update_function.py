import time
from google.cloud import pubsub_v1


def firestore_on_update_to_devices_pubsub(event, context):
    """Triggered by a change to a Firestore document.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    #name = event['value']['name']
    #state = event['value']['fields']['state']['integerValue']
    #device_id = get_device_id_from_name(name)
    #payload = '{"state": ' + state + '}'
    #if device_id is None:
    #    return

    print('test abc')
    sending_test()
    print("done sending")


def get_device_id_from_name(name):
    index_device_id = 6
    dir_tree = name.split('/')
    valid_name = len(dir_tree) is 7 and 'light_switch' in dir_tree[index_device_id]
    if valid_name:
        return dir_tree[index_device_id]
    return None


def sending_test():
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""

    # TODO(developer)
    project_id = "dankers"
    topic_id = "devices/light_switch_001/commands/#"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = dict()

    def get_callback(f, data):
        def callback(f):
            try:
                print(f.result())
                futures.pop(data)
            except:  # noqa
                print("Please handle {} for {}.".format(f.exception(), data))

        return callback

    for i in range(10):
        data = str(i)
        futures.update({data: None})
        # When you publish a message, the client returns a future.
        future = publisher.publish(
            topic_path, data=data.encode("utf-8")  # data must be a bytestring.
        )
        futures[data] = future
        # Publish failures shall be handled in the callback function.
        future.add_done_callback(get_callback(future, data))

    # Wait for all the publish futures to resolve before exiting.
    while futures:
        time.sleep(5)

    print("Published message with error handler.")


if __name__ == '__main__':
    event = {'oldValue': {'createTime': '2020-05-25T11:18:18.595997Z', 'fields': {'online': {'booleanValue': False}, 'state': {'integerValue': '0'}}, 'name': 'projects/dankers/databases/(default)/documents/devices/light_switch_001', 'updateTime': '2020-06-06T03:09:15.009407Z'}, 'updateMask': {'fieldPaths': ['state']}, 'value': {'createTime': '2020-05-25T11:18:18.595997Z', 'fields': {'online': {'booleanValue': False}, 'state': {'integerValue': '1'}}, 'name': 'projects/dankers/databases/(default)/documents/devices/light_switch_001', 'updateTime': '2020-06-06T03:09:15.009407Z'}}
    context = None
    firestore_on_update_to_devices_pubsub(event, context)
