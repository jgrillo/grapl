from grapl_cdk.event_source import EventSource
from grapl_cdk.graph_generator import GraphGenerator

from aws_cdk import core
from aws_cdk.aws_lambda import Runtime


class SysmonEvents(core.Stack):
    def __init__(self, scope: core.Construct, bucket_prefix: str, **kwargs):
        super().__init__(scope, 'sysmon-event-source', **kwargs)
        self.event_name = 'sysmon-log'
        self.event_source = EventSource.create(
            self,
            id='sysmon-event-source',
            bucket_prefix=bucket_prefix,
            event_name=self.event_name,
        )
