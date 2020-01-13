from grapl_cdk.event_source import EventSource
from grapl_cdk.graph_generator import GraphGenerator

from aws_cdk import core
from aws_cdk.aws_lambda import Runtime


class SysmonGraphGenerator(core.Stack):
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
