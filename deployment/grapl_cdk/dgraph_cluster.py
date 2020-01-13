from typing import Optional

from aws_cdk import core, aws_ec2
from aws_cdk import aws_ecs
from aws_cdk.aws_ec2 import IVpc, Port
from aws_cdk.aws_ecs import NetworkMode, CloudMapOptions, Compatibility
from aws_cdk import aws_servicediscovery
from aws_cdk.core import Duration


class Alpha(object):
    def __init__(
            self,
            scope: core.Stack,
            id: str,
            cluster_name: str,
            cluster: aws_ecs.Cluster,
            zero_address: str,
    ):
        alpha_task = aws_ecs.Ec2TaskDefinition(
            scope,
            id=id,
            network_mode=NetworkMode.AWS_VPC,
        )

        log_driver = aws_ecs.AwsLogDriver(
            stream_prefix=f'ecs{cluster_name}{id}'
        )

        alpha_task.add_container(
            id=id + cluster_name + 'Container',
            image= aws_ecs.ContainerImage.from_registry("dgraph/dgraph:1.1.1"),
            command=[
                "dgraph",
                "alpha",
                f'--my={id}.{cluster_name}.grapl:7080',
                "--lru_mb=1024",
                f'--zero=${zero_address}.{cluster_name}.grapl:5080',                                                                                                      "--alsologtostderr"
            ],
            logging=log_driver,
            memory_reservation_mib=2048,
        )

        alpha_service = aws_ecs.Ec2Service(
            scope,
            id=id + 'Service',
            cluster=cluster,
            task_definition=alpha_task,
            cloud_map_options=CloudMapOptions(
                name=id,
                dns_record_type=aws_servicediscovery.DnsRecordType.A,
                dns_ttl=Duration.seconds(300),
            )
        )

        self.name = f'{id}.{cluster_name}.grapl'

        # TODO: Restrict traffic to just the necessary dgraph ports
        alpha_service.connections.allow_from_any_ipv4(Port.all_tcp())


class Zero(object):
    def __init__(
            self,
            scope: core.Stack,
            id: str,
            cluster_name: str,
            cluster: aws_ecs.Cluster,
            peer: Optional[str],
            idx: int,
    ):
        zero_task = aws_ecs.Ec2TaskDefinition(
            scope,
            id=id,
            network_mode=NetworkMode.AWS_VPC,
        )

        command = [
            "dgraph",
            "zero",
            f"--my={id}.{cluster_name}.grapl:5080",
            "--replicas=3",
            f"--idx={idx}",
            "--alsologtostderr"
        ]
        
        if peer:
            command.append(f"--peer={peer}.{cluster_name}.grapl:5080")

        log_driver = aws_ecs.AwsLogDriver(
            stream_prefix=f'ecs{cluster_name}{id}'
        )

        zero_task.add_container(
            id=id + cluster_name + 'Container',
            image= aws_ecs.ContainerImage.from_registry("dgraph/dgraph:1.1.1"),
            command=command,
            logging=log_driver,
            memory_reservation_mib=1024,
        )


        zero_service = aws_ecs.Ec2Service(
            scope,
            id=id + 'Service',
            cluster=cluster,
            task_definition=zero_task,
            cloud_map_options=CloudMapOptions(
                name=id,
                dns_record_type=aws_servicediscovery.DnsRecordType.A,
                dns_ttl=Duration.seconds(300),
            )
        )

        self.name = f'{id}.{cluster_name}.grapl'

        # TODO: Restrict traffic to just the necessary dgraph ports
        zero_service.connections.allow_from_any_ipv4(Port.all_tcp())


class DgraphEcs(core.Stack):
    def __init__(
            self,
            scope: core.App,
            id: str,
            cluster_name: str,
            vpc: IVpc,
            zero_count: int,
            alpha_count: int,
            zero_instance_type: Optional[aws_ec2.InstanceType] = None,
            alpha_instance_type: Optional[aws_ec2.InstanceType] = None,
            **kwargs,
    ):
        super().__init__(
            scope,
            cluster_name + '-stack',
            **kwargs
        )

        if not zero_instance_type:
            zero_instance_type = aws_ec2.InstanceType("t3a.small")
        if not alpha_instance_type:
            alpha_instance_type = aws_ec2.InstanceType("t3a.medium")

        assert zero_count < 50, 'zero_count set too high, this is likely a mistake'
        assert alpha_count < 50, 'alpha_count set too high, this is likely a mistake'

        cluster = aws_ecs.Cluster(
            self,
            id=id + '-EcsCluster',
            vpc=vpc,
        )

        self.cluster = cluster

        cluster.connections.allow_internally(Port.all_tcp())

        cluster.add_default_cloud_map_namespace(
            name=f'{id}.grapl'
        )

        cluster.add_capacity(
            id=id + 'ZeroGroupCapacity',
            instance_type=zero_instance_type,
            min_capacity=zero_count,
            desired_capacity=zero_count,
            max_capacity=zero_count,
        )

        zero0 = Zero(
            self,
            id='zero0',
            cluster_name=cluster_name,
            cluster=cluster,
            peer=None,
            idx=1,
        )

        for i in range(1, zero_count):
            Zero(
                self,
                id=f'zero{i}',
                cluster_name=cluster_name,
                cluster=cluster,
                peer='zero0',
                idx=i + 1,
            )
            
        self.alpha_names = []
        
        cluster.add_capacity(
            id + 'AlphaClusterCapacity',
            instance_type=alpha_instance_type,
            min_capacity=alpha_count,
            desired_capacity=alpha_count,
            max_capacity=alpha_count,
        )

        for i in range(0, alpha_count):
            alpha = Alpha(
                self,
                id=f'alpha{i}',
                cluster_name=cluster_name,
                cluster=cluster,
                zero_address='zero0'
            )

            self.alpha_names.append(alpha.name)