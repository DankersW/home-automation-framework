# test the function with the following JSON string
# {"@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage", "attributes": {"deviceId": "light_switch_001", "deviceNumId": "2833441033873397", "deviceRegistryId": "home_automation_light_switches", "deviceRegistryLocation": "europe-west1", "projectId": "dankers"}, "data": "e2xpZ2h0c19zdGF0ZTogMX0="}

import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json


def lightswitches_pubsub_to_firebase(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    # Fetch content from pubsub event
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_device = event['attributes']['deviceId']
    message_state = None
    try:
        data = json.loads(pubsub_message)
        if 'lights_state' in data:
            message_state = data['lights_state']
    except ValueError as e:
        print("JSON conversion error in message {} -- Error: {}".format(pubsub_message, e))
    if message_state is None:
        return

    # Use the application default credentials to init firebase
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'dankers',
    })
    db = firestore.client()

    # Writing data to Firebase
    doc_ref = db.collection(u'devices').document(pubsub_device)
    doc_ref.set({
        u'online': True,
        u'state': message_state
    })


if __name__ == '__main__':
    event_arg = {'data': 'e2xpZ2h0c19zdGF0ZTogMX0=', '@type': 'type.googleapis.com/google.pubsub.v1.PubsubMessage', 'attributes': {'deviceRegistryLocation': 'europe-west1', 'deviceNumId': '2833441033873397', 'deviceRegistryId': 'home_automation_light_switches', 'deviceId': 'light_switch_001', 'projectId': 'dankers'}}
    lightswitches_pubsub_to_firebase(event_arg, None)
