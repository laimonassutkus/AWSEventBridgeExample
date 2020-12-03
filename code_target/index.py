import json


def handler(event, context):
    print(f'Received this event: {json.dumps(event)}')
