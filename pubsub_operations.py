import json
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

def publish_message(topic_path, message):

    if not isinstance(topic_path, str):
        raise ValueError('topic_path must be a string')
    if not isinstance(message, dict):
        raise ValueError('message must be a dictionary')

    future = publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
    future.result()