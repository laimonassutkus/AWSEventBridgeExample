from aws_cdk import core
from stack import Stack

app = core.App()
Stack(app, "EventBridgeTestingStack")
app.synth()
