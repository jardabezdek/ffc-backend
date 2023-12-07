from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from constructs import Construct
from stacks.utils import get_name


class Storage(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket_raw = s3.Bucket(
            self,
            id="S3BucketFrozenFactsCenterRaw",
            bucket_name=get_name("raw"),
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=False,
        )
