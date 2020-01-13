from typing import cast

from deployment.grapl_cdk.event_source import EventSource

from aws_cdk import core, aws_s3, aws_sqs, aws_lambda, aws_iam, aws_sns_subscriptionss
from aws_cdk.core import PhysicalName
from aws_cdk.aws_ec2 import IVpc, Vpc
from aws_cdk.aws_lambda import Code, Runtime
from aws_cdk.aws_sns import ITopicSubscription


class GraplService(object):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            vpc: IVpc,
            handler_path: str,
            handler='main.lambda_handler'
    ):
        self.vpc = vpc
        self.scope = scope
        self.queue = aws_sqs.Queue(
            scope=scope,
            id='source_queue' + id,
            queue_name=PhysicalName.GENERATE_IF_NEEDED,
        )

        self.fn = aws_lambda.Function(
            scope,
            id + 'service',
            code=Code.from_asset(handler_path),
            handler=handler,
            runtime=Runtime.PYTHON_3_7,
            vpc=vpc,
        )

    def triggered_by(self, event_source: EventSource) -> 'GraplService':
        policy = aws_iam.PolicyStatement()

        policy.add_actions('s3:GetObject')
        policy.add_resources(event_source.bucket.bucket_arn)

        self.fn.add_to_role_policy(policy)

        dest = cast(
            ITopicSubscription,
            aws_sns_subscriptions.SqsSubscription(
                queue=self.queue,
                raw_message_delivery=True,
            )
        )

        event_source.topic.add_subscription(
            subscription=dest
        )

        return self

    def output_to(self, dest_bucket: aws_s3.Bucket) -> 'GraplService':
        dest_bucket.grant_write(self.fn)
        return self
