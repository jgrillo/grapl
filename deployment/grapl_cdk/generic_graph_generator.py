from deployment.grapl_cdk.graph_generator import GraphGenerator

from aws_cdk import aws_core
from aws_cdk.aws_lambda import Runtime


class SysmonGraphGenerator(aws_core.Stack):
    def __init__(
            self,
            bucket_prefix: str,
    ):
        self.graph_generator = GraphGenerator(
            scope=self,
            id='sysmon-subgraph-generator',
            bucket_prefix=bucket_prefix,
            event_name='sysmon-log',
            handler_path='./sysmonsubgraph-generator.zip',
            runtime=Runtime.Custom,
            handler='main.lambda_handler'
        )