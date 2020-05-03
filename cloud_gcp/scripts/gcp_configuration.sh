PROJECT_ID="dankers"
REGION="europe-west1"

# Creating a device registry
REGISTRY_ID="home_automation_light_switches"
EVENT_PUBSUB_TOPIC="home_automation_light_switches_event_topic"
STATE_PUBSUB_TOPIC="home_automation_light_switches_state_topic"
gcloud iot registries create ${REGISTRY_ID} --project=${PROJECT_ID} --region=${REGION} --enable-mqtt-config --no-enable-http-config --event-notification-config=topic=${EVENT_PUBSUB_TOPIC} --state-pubsub-topic=${STATE_PUBSUB_TOPIC}

# Creating public/private key pairs
mkdir -p certificates
openssl genpkey -algorithm RSA -out certificates/rsa_light_switch_private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in certificates/rsa_light_switch_private.pem -pubout -out certificates/rsa_light_switch_public.pem
wget https://pki.goog/roots.pem

# Create a device
DEVICE_ID="light_switch_001"
gcloud iot devices create ${DEVICE_ID} --project=${PROJECT_ID} --region=${REGION} --registry=${REGISTRY_ID} --log-level=info --public-key path=/home/wouter_dankers/certificates/rsa_light_switch_public.pem,type=rsa-pem

# Create the pubsub topics
gcloud pubsub topics create ${EVENT_PUBSUB_TOPIC} --project=${PROJECT_ID}
gcloud pubsub topics create ${STATE_PUBSUB_TOPIC} --project=${PROJECT_ID}

# Create test subsription for testing
SUBSCRIPTION_ID="test_home_automation_light_switches_event_subsription"
gcloud pubsub subscriptions create ${SUBSCRIPTION_ID} --topic=${EVENT_PUBSUB_TOPIC} --project=${PROJECT_ID}
gcloud pubsub subscriptions pull --auto-ack projects/${PROJECT_ID}/subscriptions/${SUBSCRIPTION_ID} --limit=100

