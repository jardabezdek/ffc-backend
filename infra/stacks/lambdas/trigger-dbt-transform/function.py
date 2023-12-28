"""Lambda function that triggers ECS task to transform data."""

import os
from typing import Any

import boto3

ECS_CLUSTER_ARN = os.environ["ECS_CLUSTER_ARN"]
ECS_TASK_DEFINITION_ARN = os.environ["ECS_TASK_DEFINITION_ARN"]
ECS_CONTAINER_NAME = os.environ["ECS_CONTAINER_NAME"]
ECS_SUBNET_IDS = os.environ["ECS_SUBNET_IDS"]
ECS_SECURITY_GROUP_ID = os.environ["ECS_SECURITY_GROUP_ID"]

ecs = boto3.client("ecs")


def handler(event: dict, context: Any) -> dict:
    """Trigger ECS task to transform data.

    Parameters:
    -----------
    event: dict
        A dictionary that contains data for a Lambda function to process.
    context: Any
        An object that provides methods and properties that provide information about
        the invocation, function, and runtime environment.

    Returns:
    --------
    dict
    """
    try:
        response = ecs.run_task(
            cluster=ECS_CLUSTER_ARN,
            taskDefinition=ECS_TASK_DEFINITION_ARN,
            count=1,
            launchType="FARGATE",
            overrides={
                "containerOverrides": [
                    {
                        "name": ECS_CONTAINER_NAME,
                    },
                ],
            },
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": ECS_SUBNET_IDS.split(","),
                    "securityGroups": [ECS_SECURITY_GROUP_ID],
                    "assignPublicIp": "ENABLED",
                }
            },
        )

        print(response)
        return {"status_code": 200, "body": "✅ ECS task has been triggered!"}

    except Exception as exc:
        return {"status_code": 500, "body": f"❌ Internal server error: {exc}"}
