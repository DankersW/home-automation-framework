# following Google's strict structuring convention
# For the Python runtime, your function's entry-point must be defined in a Python
# source file at the root of your project named main.py.

import base64


def print_mqtt_pubsub_data(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)