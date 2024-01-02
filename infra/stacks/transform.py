from pathlib import Path

from aws_cdk import (
    Stack,
    aws_ec2,
    aws_ecr_assets,
    aws_ecs,
    aws_events,
    aws_events_targets,
    aws_iam,
)
from constructs import Construct
from stacks.utils import get_name


class Transform(Stack):
    """Stack used for dbt transformation."""

    frequency_cron_transform = {"minute": "15", "hour": "7"}
    task_cpu = "1024"
    task_memory_mib = "2048"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = self.create_vpc()
        self.cluster = self.create_ecs_cluster()
        self.image = self.create_image()
        self.task = self.create_task()

    def create_vpc(self) -> aws_ec2.Vpc:
        """Create a Virtual Private Cloud for the transformation stack.

        Returns:
        --------
        aws_ec2.Vpc
            The configured VPC.
        """
        return aws_ec2.Vpc(
            self,
            id="VpcTransform",
            vpc_name=get_name("vpc-transform"),
            max_azs=2,
        )

    def create_ecs_cluster(self) -> aws_ecs.Cluster:
        """Create an Elastic Container Service cluster for the transformation stack.

        Returns:
        --------
        aws_ecs.Cluster
            The configured ECS cluster for transformation.
        """
        return aws_ecs.Cluster(
            self,
            id="ECSClusterTransform",
            cluster_name=get_name("ecs-cluster-transform"),
            container_insights=True,
            vpc=self.vpc,
        )

    def create_image(self):
        """Create a Docker image asset for the ECR repository in the transformation stack.

        Returns:
        --------
        aws_ecr_assets.DockerImageAsset
            The Docker image asset for the ECR repository.
        """
        return aws_ecr_assets.DockerImageAsset(
            self,
            id="ECRImageTransform",
            asset_name=get_name("ecr-image-transform"),
            directory=(Path(__file__).resolve().parent.parent / "transform").as_posix(),
            platform=aws_ecr_assets.Platform.LINUX_AMD64,
        )

    def create_task(self):
        """Create an Elastic Container Service task definition for transformation.

        Returns:
        --------
        aws_ecs.TaskDefinition
            The ECS task definition for the transformation task.
        """
        task = aws_ecs.TaskDefinition(
            self,
            id="ECSTaskDefinitionTransform",
            family=get_name("ecs-task-runner-transform"),
            compatibility=aws_ecs.Compatibility.FARGATE,
            cpu=self.task_cpu,
            memory_mib=self.task_memory_mib,
        )

        # add ECS task permissions to communicate with S3
        task.add_to_task_role_policy(
            statement=aws_iam.PolicyStatement(
                actions=[
                    "ecs:StartTelemetrySession",
                    "s3:*",
                ],
                effect=aws_iam.Effect.ALLOW,
                resources=["*"],
            )
        )

        # add the docker container to the task
        task.add_container(
            id="ECSContainerTransform",
            container_name=get_name("ecs-container-transform"),
            image=aws_ecs.ContainerImage.from_docker_image_asset(asset=self.image),
            logging=aws_ecs.LogDriver.aws_logs(stream_prefix=get_name("ecs-log-transform")),
        )

        # schedule ECS task to run on regular basis
        event_rule = aws_events.Rule(
            self,
            id="TransformScheduleRule",
            rule_name=get_name("rule-transform"),
            schedule=aws_events.Schedule.cron(**self.frequency_cron_transform),
        )
        event_rule.add_target(
            target=aws_events_targets.EcsTask(cluster=self.cluster, task_definition=task)
        )

        return task
