"""
Lambda function to download a games schedule for the next 7 days, and save it into S3 bucket as a PARQUET file.
"""

import json
import os
from enum import Enum
from typing import Any

import boto3
import pandas as pd
import requests

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]
URL_SCHEDULE = "https://api-web.nhle.com/v1/schedule/now"

s3 = boto3.resource("s3")


class SeasonType(Enum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFF = 3
    ALLSTAR = 4


def handler(event: dict, context: Any) -> None:
    """Download and save a games schedule.

    Parameters:
    -----------
    event: dict
        A dictionary that contains data for a Lambda function to process.
    context: Any
        An object that provides methods and properties that provide information about
        the invocation, function, and runtime environment.

    Returns:
    --------
    None
    """
    try:
        # call NHL API
        response = requests.get(url=URL_SCHEDULE)
        schedule = json.loads(response.text)

        # parse games from schedule
        games = [
            {
                "id": game.get("id"),
                "season": game.get("season"),
                "venue": game.get("venue", {}).get("default"),
                "day": day.get("date"),
                "start_time_utc": game.get("startTimeUTC"),
                "home_team_id": game.get("homeTeam", {}).get("id"),
                "away_team_id": game.get("awayTeam", {}).get("id"),
            }
            for day in schedule.get("gameWeek")
            for game in day.get("games")
            if game.get("gameType") in [SeasonType.REGULAR.value, SeasonType.PLAYOFF.value]
            and game.get("gameState") == "FUT"
        ]

        if not games:
            games = [
                {
                    "id": None,
                    "season": None,
                    "venue": None,
                    "day": None,
                    "start_time_utc": None,
                    "home_team_id": None,
                    "away_team_id": None,
                }
            ]
            print("❌ No games scheduled.")

        # save data into destination bucket
        path = f"s3://{DESTINATION_BUCKET}/schedule/schedule.parquet"
        pd.DataFrame(games).to_parquet(path=path, index=False)
        print(f"✅ Saved schedule into `{path}` successfully!")

    except Exception as exc:
        print(f"❌ Internal server error: {exc}")
