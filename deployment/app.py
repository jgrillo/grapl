#!/usr/bin/env python3

from aws_cdk import core

from grapl_cdk.grapl_cdk_stack import GraplCdkStack


app = core.App()
GraplCdkStack(app, "grapl-cdk")

app.synth()
