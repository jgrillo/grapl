from aws_cdk import aws_elasticache
from aws_cdk.aws_ec2 import Vpc, SecurityGroup, Connections, Port
from aws_cdk.core import Construct, Stack


class GraplVpc(Stack):
    def __init__(
            self,
            scope: Construct,
            **kwargs
    ) -> None:
        super(GraplVpc, self).__init__(scope, 'graplvpcs-stack', **kwargs)
        self.grapl_vpc = Vpc(
            self,
            'GraplVPC',
            nat_gateways=1,
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )