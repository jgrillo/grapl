from aws_cdk import aws_elasticache
from aws_cdk.aws_ec2 import IVpc, SecurityGroup, Connections, Port
from aws_cdk.core import Construct


class RedisCluster(object):
    def __init__(
            self,
            scope: Construct,
            id: str,
            vpc: IVpc,
            cluster_size: int,
    ) -> None:
        subnet_group = aws_elasticache.CfnSubnetGroup(
            scope,
            id=f'{id}-subnetgroup',
            cache_subnet_group_name=f'{id}-subnetgroup',
            description='List of subnets for {id}',
            subnet_ids=[
                subnet.subnet_id for subnet in vpc.private_subnets
            ],
        )

        self.security_group = SecurityGroup(
            scope,
            id=f'{id}-securitygroup',
            vpc=vpc,
        )

        self.connections = Connections(
            security_groups=[self.security_group],
            default_port=Port.tcp(6379),
        )

        self.cluster = aws_elasticache.CfnCacheCluster(
            scope,
            id=f'{id}-cachecluster',
            cache_node_type='cache.t2.small',
            engine='redis',
            num_cache_nodes=cluster_size,
            auto_minor_version_upgrade=True,
            cache_subnet_group_name=subnet_group.cache_subnet_group_name,
            vpc_security_group_ids=[
                self.security_group.security_group_id
            ]
        )