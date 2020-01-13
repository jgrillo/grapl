import os

from aws_cdk import core, aws_s3, aws_sns


class EventSource(object):
    def __init__(
        self,
        scope: core.Construct,
        topic: aws_sns.Topic,
        bucket: aws_s3.Bucket,
    ):
        self.scope = scope
        self.topic = topic
        self.bucket = bucket

    @staticmethod
    def create(
            scope,
            id,
            bucket_prefix: str,
            event_name: str,
    ) -> 'EventSource':
        topic = aws_sns.Topic(
            scope,
            id + 'source_topic',
        )

        bucket = aws_s3.Bucket(
            scope,
            id + 'source_bucket',
            bucket_name=f'{bucket_prefix}-{event_name}-bucket'
        )

        return EventSource(scope, topic, bucket)

    @staticmethod
    def import_from(
            scope,
            id,
            bucket_prefix: str,
            event_name: str,
    ) -> 'EventSource':
        region = os.environ["CDK_DEFAULT_REGION"]
        account_id = os.environ["CDK_DEFAULT_ACCOUNT"]
        sns_arn = f"arn:aws:sns:{region}:{account_id}:{event_name}-topic"

        topic = aws_sns.Topic.from_topic_arn(
            scope,
            id + 'source_topic',
            topic_arn=sns_arn,
        )

        bucket = aws_s3.Bucket.from_bucket_name(
            scope,
            id + 'source_bucket',
            bucket_name=f'{bucket_prefix}-{event_name}-bucket'
        )

        return EventSource(
            scope, topic, bucket
        )
