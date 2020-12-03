from typing import Union
from aws_cdk import core
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.aws_events import EventBus, Rule, EventPattern, IRuleTarget
from aws_cdk.aws_events_targets import LambdaFunction


class Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.event_bus = EventBus(
            scope=self,
            id='CustomEventBus',
            event_bus_name='CustomEventBus'
        )

        self.source = Function(
            scope=self,
            id=f'SourceFunction',
            function_name=f'SourceFunction',
            code=Code.from_asset(path='./code_source/'),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_6,
        )

        self.source.add_to_role_policy(statement=PolicyStatement(
            actions=['events:PutEvents'],
            resources=[self.event_bus.event_bus_arn]
        ))

        """
        Define rule.
        """

        self.rule = Rule(
            scope=self,
            id='EventBusRule',
            description='Sample description.',
            enabled=True,
            event_bus=self.event_bus,
            event_pattern=EventPattern(
                detail={
                    'Domain': ["MedInfo"],
                    'Reason': ["InvokeTarget"]
                }
            ),
            rule_name='EventBusRule',
        )

        """
        Add target.
        """

        self.target = Function(
            scope=self,
            id=f'TargetFunction',
            function_name=f'TargetFunction',
            code=Code.from_asset(path='./code_target/'),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_6,
        )

        self.target: Union[IRuleTarget, LambdaFunction] = LambdaFunction(handler=self.target)
        self.rule.add_target(target=self.target)
