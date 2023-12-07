#!/usr/bin/env python3

import os

import aws_cdk as cdk
from stacks import Compute, Storage

app = cdk.App()

storage_stack = Storage(
    scope=app,
    construct_id="StorageStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

compute_stack = Compute(
    scope=app,
    construct_id="ComputeStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
    storage_stack=storage_stack,
)

app.synth()
