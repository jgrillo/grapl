from deployment.grapl_cdk.graph_generator import GraphGenerator

from aws_cdk import aws_core
from aws_cdk.aws_lambda import Runtime

from deployment.grapl_cdk.sysmon_events import SysmonEvents


class SysmonGraphGenerator(aws_core.Stack):
    def __init__(
            self,
            bucket_prefix: str,
            sysmon_events: SysmonEvents
    ):
        self.graph_generator = GraphGenerator(
            scope=self,
            id='sysmon-subgraph-generator',
            bucket_prefix=bucket_prefix,
            event_name=sysmon_events.event_name,
            handler_path='./sysmonsubgraph-generator.zip',
            runtime=Runtime.Custom,
            handler='main.lambda_handler'
        )