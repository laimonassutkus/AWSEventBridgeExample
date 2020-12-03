import json
import boto3

client = boto3.client('events')


def handler(event, context):
    print(f'Received this event: {json.dumps(event)}')

    response = client.put_events(
        Entries=[
            dict(
                Source='CustomSource',
                Detail=json.dumps(dict(
                    Domain="MedInfo",
                    Reason="InvokeTarget",
                    Description="Sample description.",
                    Schema="1.0.0",
                    Version="0.0.1",
                )),
                DetailType='CustomDetailType',
                EventBusName='CustomEventBus'
            )
        ]
    )

    errors = '\n'.join(entry.get('ErrorMessage') for entry in response['Entries'])
    assert response['FailedEntryCount'] == 0, errors
