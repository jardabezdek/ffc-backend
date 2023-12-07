from pathlib import Path

from aws_cdk import Duration, Stack, aws_events, aws_events_targets, aws_lambda
from constructs import Construct
from stacks.utils import get_name


class Compute(Stack):
    """Stack for computing resources."""

    frequency_cron_download_raw_games = {"minute": "0", "hour": "7"}

    def __init__(self, scope: Construct, construct_id: str, storage_stack: Stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_hello_world = self.create_lambda_hello_world()
        self.lambda_download_raw_games = self.create_lambda_download_raw_games(
            storage_stack=storage_stack
        )

    def create_lambda_hello_world(self) -> aws_lambda.DockerImageFunction:
        """Create a Docker container-based AWS Lambda function as an example.

        Returns:
        --------
        aws_lambda.DockerImageFunction
            The Docker container-based Lambda function for Hello World.
        """
        return aws_lambda.DockerImageFunction(
            self,
            id="LambdaHelloWorld",
            function_name=get_name("hello-world"),
            description="Example lambda function.",
            code=aws_lambda.DockerImageCode.from_image_asset(
                (Path(__file__).resolve().parent / "lambdas" / "hello-world").as_posix()
            ),
            architecture=aws_lambda.Architecture.X86_64,
            memory_size=128,
            timeout=Duration.seconds(10),
            environment={
                "THE_ENVIRONMENT_VARIABLE": "The environment variable value.",
            },
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
            timeout=Duration.seconds(90),
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
