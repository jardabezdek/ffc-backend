"""Lambda function to download a teams metadata as PARQUET file, and save them into S3 bucket."""

import os
from typing import Any

import boto3
import pandas as pd

from utils import get_current_standings

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]

s3 = boto3.resource("s3")


def handler(event: dict, context: Any) -> dict:
    """Download and save a teams data as PARQUET file.

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
        standings = get_current_standings()
        path = f"s3://{DESTINATION_BUCKET}/teams.parquet"
        (
            pd.DataFrame(
                [
                    {
                        "team_full_name": standing.get("teamName").get("default"),
                        "team_abbrev_name": standing.get("teamAbbrev").get("default"),
                        "team_common_name": standing.get("teamCommonName").get("default"),
                        "conference": standing.get("conferenceName"),
                        "conference_abbrev": standing.get("conferenceAbbrev"),
                        "division": standing.get("divisionName"),
                        "division_abbrev": standing.get("divisionAbbrev"),
                        "team_logo_url": standing.get("teamLogo"),
                    }
                    for standing in standings
                ]
            )
            .sort_values(by=["conference", "division", "team_full_name"])
            .to_parquet(path=path, index=False)
        )

        print(f"ℹ️ Saved `{path}` successfully!")
        return {"status_code": 200, "body": "✅ Teams data downloaded successfully!"}

    except Exception as exc:
        return {"status_code": 500, "body": f"❌ Internal server error: {exc}."}
