from deployment.grapl_cdk.grapl_service import GraplService
from deployment.grapl_cdk.event_source import EventSource

from aws_cdk import aws_core, aws_s3
from aws_cdk.aws_ec2 import IVpc, Vpc
from aws_cdk.aws_lambda import Runtime


class GeneratedUnidGraphsBucket(object):
    def __init__(self, scope: aws_core.Construct, bucket_prefix: str):
        self.bucket = aws_s3.Bucket.from_bucket_name(
            scope,
            id='GeneratedUnidGraphsBucked',
            bucket_name=f'{bucket_prefix}-unid-subgraphs-generated-bucket'
        )
        self.bucket_name = self.bucket.bucket_name


class GraphGenerator(GraplService):
    def __init__(
            self,
            scope: aws_core.Construct,
            id: str,
            bucket_prefix: str,
            event_name: str,
            handler_path: str,
            runtime: Runtime,
            handler='main.lambda_handler'
    ):
        super().__init__(
            scope=scope,
            id=id,
            vpc=Vpc.from_lookup(scope, id=f'{id}Vpc', vpc_name=f'{bucket_prefix}vpcs-stack/GraplVPC'),
            handler_path=handler_path,
            runtime=runtime,
            handler=handler,
        )

        self.source_bucket = EventSource.import_from(
            scope,
            id,
            bucket_prefix,
            event_name,
        )

        self.dest_bucket = GeneratedUnidGraphsBucket(scope, bucket_prefix)

        self.triggered_by(self.source_bucket)
        self.output_to(self.dest_bucket.bucket)
