from deployment.grapl_cdk.event_source import EventSource
from deployment.grapl_cdk.graph_generator import GraphGenerator

from aws_cdk import aws_core
from aws_cdk.aws_lambda import Runtime


class SysmonEvents(aws_core.Stack):
    def __init__(self, bucket_prefix: str):

        self.event_name = 'sysmon-log'
        self.event_source = EventSource.create(
            self,
            id='sysmon-event-source',
            bucket_prefix=bucket_prefix,
            event_name=self.event_name,
        )
