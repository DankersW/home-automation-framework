# Notes
Mostly good to remember cli commands

## Cloud pub/sub
Pull messages from a specific subscription
```shell
gcloud pubsub subscriptions pull --auto-ack projects/dankers/subscriptions/test-led-subscription --limit=100
```