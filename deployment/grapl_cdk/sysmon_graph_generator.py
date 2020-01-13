from aws_cdk.aws_ec2 import IVpc
from aws_cdk.core import Construct
from grapl_cdk.graph_generator import GraphGenerator

from aws_cdk import core
from aws_cdk.aws_lambda import Runtime

from grapl_cdk.sysmon_events import SysmonEvents
from redis_cluster import RedisCluster


class SysmonGraphGenerator(core.Stack):
    def __init__(
            self,
            scope: Construct,
            bucket_prefix: str,
            sysmon_events: SysmonEvents,
            vpc: IVpc,
            cache_cluster_size: int = 1,
            **kwargs,
    ):
        super().__init__(
            scope,
            'sysmon-subgraph-generator',
            **kwargs
        )

        self.cache = RedisCluster(
            self,
            'sysmon-subgraph-generator',
            vpc=vpc,
            cluster_size=cache_cluster_size,
        )

        self.graph_generator = GraphGenerator(
            scope=self,
            id='sysmon-subgraph-generator',
            bucket_prefix=bucket_prefix,
            event_name=sysmon_events.event_name,
            handler_path='./sysmon-subgraph-generator.zip',
            runtime=Runtime.PROVIDED,
            handler='sysmon-subgraph-generator.lambda_handler',
            environment={
                'EVENT_CACHE_ADDR': self.cache.cluster.attr_redis_endpoint_address,
            }
        )
