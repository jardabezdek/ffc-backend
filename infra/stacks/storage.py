from aws_cdk import Stack, aws_s3
from constructs import Construct
from stacks.utils import get_name


class Storage(Stack):
    """Stack with data storage services."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket_raw = self.create_bucket_raw()
        self.bucket_base = self.create_bucket_base()

    def create_bucket_raw(self) -> aws_s3.Bucket:
        """Create an S3 bucket for raw data storage. Raw data reflect the data from NHL API. They
        are stored in the JSON format.

        Returns:
        --------
        aws_s3.Bucket
            The S3 bucket for raw data storage.
        """
        return aws_s3.Bucket(
            self,
            id="S3BucketFrozenFactsCenterRaw",
            bucket_name=get_name("raw"),
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=False,
        )

    def create_bucket_base(self) -> aws_s3.Bucket:
        """Create an S3 bucket for base data storage. Base data are cleansed and renamed raw data.
        They are stored in the PARQUET format.

        Returns:
        --------
        s3.Bucket
            The S3 bucket for raw data storage.
        """
        return aws_s3.Bucket(
            self,
            id="S3BucketFrozenFactsCenterBase",
            bucket_name=get_name("base"),
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            versioned=False,
        )
