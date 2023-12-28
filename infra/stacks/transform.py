from pathlib import Path

from aws_cdk import Stack, aws_ec2, aws_ecr_assets, aws_ecs, aws_lambda
from constructs import Construct
from stacks.utils import get_env_variables, get_name


class Transform(Stack):
    """Stack used for dbt transformation."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create VPC
        self.vpc_transform = aws_ec2.Vpc(
            self,
            id="VpcTransform",
            vpc_name=get_name("vpc-transform"),
            nat_gateways=2,
            max_azs=2,
        )

        # create security group
        self.security_group_transform = aws_ec2.SecurityGroup(
            self,
            id="SecurityGroupTransform",
            vpc=self.vpc_transform,
            security_group_name=get_name("security-group-transform"),
            allow_all_outbound=True,
        )

        # create ECS cluster to deploy tasks to
        self.ecs_cluster = aws_ecs.Cluster(
            self,
            id="ECSClusterTransform",
            cluster_name=get_name("ecs-cluster-transform"),
            container_insights=True,
            vpc=self.vpc_transform,
        )

        # add ECS task for defining provisioning of resources
        self.ecs_task_runner = aws_ecs.TaskDefinition(
            self,
            id="ECSTaskDefinitionTransform",
            family=get_name("ecs-task-runner-transform"),
            compatibility=aws_ecs.Compatibility.FARGATE,
            cpu="1024",
            memory_mib="2048",
        )

        # create image
        self.ecr_image_transform = aws_ecr_assets.DockerImageAsset(
            self,
            id="ECRImageTransform",
            asset_name=get_name("ecr-image-transform"),
            directory=(Path(__file__).resolve().parent.parent / "transform").as_posix(),
            platform=aws_ecr_assets.Platform.LINUX_AMD64,
            build_args=get_env_variables(),
            invalidation=aws_ecr_assets.DockerImageAssetInvalidationOptions(build_args=False),
        )

        # add the docker container to the task
        self.ecs_container = self.ecs_task_runner.add_container(
            id="ECSContainerTransform",
            container_name=get_name("ecs-container-transform"),
            image=aws_ecs.ContainerImage.from_docker_image_asset(asset=self.ecr_image_transform),
            logging=aws_ecs.LogDriver.aws_logs(stream_prefix=get_name("ecs-log-transform")),
        )

        # create a lambda function used to trigger the task to start
        self.lambda_trigger = aws_lambda.Function(
            self,
            id="LambdaTransformTrigger",
            function_name=get_name("trigger-transform"),
            description="Trigger dbt transformation.",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            code=aws_lambda.Code.from_asset(
                (Path(__file__).resolve().parent / "lambdas" / "trigger-dbt-transform").as_posix()
            ),
            handler="function.handler",
            environment={
                "ECS_CLUSTER_ARN": self.ecs_cluster.cluster_arn,
                "ECS_TASK_DEFINITION_ARN": self.ecs_task_runner.task_definition_arn,
                "ECS_CONTAINER_NAME": self.ecs_container.container_name,
                "ECS_SUBNET_IDS": ",".join(
                    self.vpc_transform.select_subnets(
                        subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT
                    ).subnet_ids
                ),
                "ECS_SECURITY_GROUP_ID": self.security_group_transform.security_group_id,
            },
        )

        # grant lambda function the permissions to run task
        self.ecs_task_runner.grant_run(grantee=self.lambda_trigger)
