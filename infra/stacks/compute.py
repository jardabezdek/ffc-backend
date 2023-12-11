from pathlib import Path

from aws_cdk import (
    Duration,
    Stack,
    aws_events,
    aws_events_targets,
    aws_lambda,
    aws_s3,
    aws_s3_notifications,
)
from constructs import Construct
from stacks.utils import get_name


class Compute(Stack):
    """Stack with compute services."""

    frequency_cron_download_raw_games = {"minute": "0", "hour": "7"}

    def __init__(self, scope: Construct, construct_id: str, storage_stack: Stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_download_raw_games = self.create_lambda_download_raw_games(
            storage_stack=storage_stack
        )
        self.lambda_transform_raw_to_base = self.create_lambda_transform_raw_to_base(
            storage_stack=storage_stack
        )

    def create_lambda_download_raw_games(
        self, storage_stack: Stack
    ) -> aws_lambda.DockerImageFunction:
        """Create a Docker container-based AWS Lambda function to download raw games.

        Parameters:
        -----------
        self : instance
            The instance of the class.
        storage_stack : Stack
            The stack containing the destination bucket.

        Returns:
        --------
        aws_lambda.DockerImageFunction
            The Docker container-based Lambda function to download raw games.
        """
        lambda_download_raw_games = aws_lambda.DockerImageFunction(
            self,
            id="LambdaDownloadRawGames",
            function_name=get_name("download-raw-games"),
            description="Download raw games data from NHL API.",
            code=aws_lambda.DockerImageCode.from_image_asset(
                (Path(__file__).resolve().parent / "lambdas" / "download-raw-games").as_posix()
            ),
            architecture=aws_lambda.Architecture.X86_64,
            timeout=Duration.seconds(60),
            environment={
                "DESTINATION_BUCKET": storage_stack.bucket_raw.bucket_name,
            },
        )

        # grant lambda function the permissions to read/write from/to the S3 bucket
        storage_stack.bucket_raw.grant_read_write(identity=lambda_download_raw_games)

        # schedule lambda function to run on regular basis
        event_rule = aws_events.Rule(
            self,
            id="LambdaDownloadRawGamesScheduleRule",
            schedule=aws_events.Schedule.cron(**self.frequency_cron_download_raw_games),
        )
        event_rule.add_target(aws_events_targets.LambdaFunction(handler=lambda_download_raw_games))

        return lambda_download_raw_games

    def create_lambda_transform_raw_to_base(
        self, storage_stack: Stack
    ) -> aws_lambda.DockerImageFunction:
        """Create a Docker container-based AWS Lambda function to transform raw data into base data.

        Parameters:
        -----------
        self : instance
            The instance of the class.
        storage_stack : Stack
            The stack containing the destination bucket.

        Returns:
        --------
        aws_lambda.DockerImageFunction
            The Docker container-based Lambda function to transform raw data into base data.
        """
        lambda_transform_raw_to_base = aws_lambda.DockerImageFunction(
            self,
            id="LambdaTransformRawToBase",
            function_name=get_name("transform-raw-to-base"),
            description="Transform raw data into base data.",
            code=aws_lambda.DockerImageCode.from_image_asset(
                (Path(__file__).resolve().parent / "lambdas" / "transform-raw-to-base").as_posix()
            ),
            architecture=aws_lambda.Architecture.X86_64,
            timeout=Duration.seconds(60),
            environment={
                "DESTINATION_BUCKET": storage_stack.bucket_base.bucket_name,
            },
        )

        # grant lambda function the permissions to read/write from/to the S3 buckets
        storage_stack.bucket_raw.grant_read(identity=lambda_transform_raw_to_base)
        storage_stack.bucket_base.grant_read_write(identity=lambda_transform_raw_to_base)

        # trigger lambda function when a new file is added into raw bucket
        bucket_raw = aws_s3.Bucket.from_bucket_name(
            self,
            id="S3BucketFrozenFactsCenterBaseFromName",
            bucket_name=storage_stack.bucket_raw.bucket_name,
        )
        bucket_raw.add_event_notification(
            aws_s3.EventType.OBJECT_CREATED_PUT,
            aws_s3_notifications.LambdaDestination(fn=lambda_transform_raw_to_base),
            aws_s3.NotificationKeyFilter(prefix="games/", suffix=".json"),
        )

        return lambda_transform_raw_to_base
