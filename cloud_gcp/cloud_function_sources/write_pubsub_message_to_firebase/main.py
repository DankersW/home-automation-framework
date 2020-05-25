import base64
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    # pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    # print(pubsub_message)
    print("start!!")

    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'dankers',
    })
    db = firestore.client()

    # Writing data
    doc_ref = db.collection(u'users').document(u'aturing')
    doc_ref.set({
        u'first': u'Alan',
        u'middle': u'Mathison',
        u'last': u'Turing',
        u'born': 1912
    })

    # Reading data
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    print("Done ")