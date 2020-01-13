#!/usr/bin/env python3

import os

from aws_cdk import core, aws_ec2
from dgraph_cluster import DgraphEcs

from grapl_cdk.sysmon_events import SysmonEvents
from grapl_cdk.sysmon_graph_generator import SysmonGraphGenerator
from grapl_vpc import GraplVpc

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')

app = core.App()

# bucket_prefix = os.environ['BUCKET_PREFIX']

bucket_prefix = os.environ['BUCKET_PREFIX']

master_zero_count = os.environ.get('MASTER_ZERO_COUNT', 1)
master_alpha_count = os.environ.get('MASTER_ALPHA_COUNT', 1)

master_zero_instance_type = os.environ.get('MASTER_ZERO_INSTANCE_TYPE', None)
master_alpha_instance_type = os.environ.get('MASTER_ALPHA_INSTANCE_TYPE', None)

engagement_zero_count = os.environ.get('ENGAGEMENT_ZERO_COUNT', 1)
engagement_alpha_count = os.environ.get('ENGAGEMENT_ALPHA_COUNT', 1)

engagement_zero_instance_type = os.environ.get('ENGAGEMENT_ZERO_INSTANCE_TYPE', None)
engagement_alpha_instance_type = os.environ.get('ENGAGEMENT_ALPHA_INSTANCE_TYPE', None)


if master_zero_instance_type:
    master_zero_instance_type = aws_ec2.InstanceType(master_zero_instance_type)

if master_alpha_instance_type:
    master_alpha_instance_type = aws_ec2.InstanceType(master_alpha_instance_type)

if engagement_zero_instance_type:
    engagement_zero_instance_type = aws_ec2.InstanceType(engagement_zero_instance_type)

if engagement_alpha_instance_type:
    engagement_alpha_instance_type = aws_ec2.InstanceType(engagement_alpha_instance_type)


env=core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]
)

grapl_vpc = GraplVpc(app, env=env)

sysmon_events = SysmonEvents(
    app,
    bucket_prefix=bucket_prefix,
    env=env,
)

SysmonGraphGenerator(
    app,
    bucket_prefix=bucket_prefix,
    sysmon_events=sysmon_events,
    vpc=grapl_vpc.grapl_vpc,
    env=env,
)

master_graph = DgraphEcs(
    scope=app,
    id='mastergraphcluster',
    cluster_name='mastergraphcluster',
    vpc=grapl_vpc.grapl_vpc,
    zero_count=master_zero_count,
    alpha_count=master_alpha_count,
    zero_instance_type=master_zero_instance_type,
    alpha_instance_type=master_alpha_instance_type,
    env=env,
)

engagement_graph = DgraphEcs(
    scope=app,
    id='engagementgraphcluster',
    cluster_name='engagementgraphcluster',
    vpc=grapl_vpc.grapl_vpc,
    zero_count=engagement_zero_count,
    alpha_count=engagement_alpha_count,
    zero_instance_type=engagement_zero_instance_type,
    alpha_instance_type=engagement_alpha_instance_type,
    env=env,
)

app.synth()
