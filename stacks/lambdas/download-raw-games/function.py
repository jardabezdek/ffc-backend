"""
Lambda function to download a game's play-by-play and game metadata as JSON files,
and save them into S3 bucket.
"""

import json
import os
from typing import Any

import boto3
import requests
from utils import SeasonType, extract_info_from, get_yesterday_game_ids

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]
URL_GAMECENTER = "https://api-web.nhle.com/v1/gamecenter"
URL_SHIFTCHART = "https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId="

s3 = boto3.resource("s3")


def handler(event: dict, context: Any) -> None:
    """Download and save a game data and shift chart as JSON files based on the game ID.

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
    yesterday_game_ids = get_yesterday_game_ids()

    if not yesterday_game_ids:
        print("❌ No game ids returned from NHL API.")
        return

    for game_id in yesterday_game_ids:
        season, season_type = extract_info_from(game_id=game_id)

        # download only regular season and play-off games
        if season_type not in [
            SeasonType.REGULAR.name.lower(),
            SeasonType.PLAYOFF.name.lower(),
        ]:
            continue

        # call NHL API endpoints
        for url, data_type, s3_key in [
            (
                f"{URL_GAMECENTER}/{game_id}/play-by-play",
                "game data",
                f"games/{season}/{season_type}/{game_id}.json",
            ),
            (
                f"{URL_SHIFTCHART}{game_id}",
                "shift chart",
                f"shift-charts/{season}/{season_type}/{game_id}.json",
            ),
        ]:
            response = requests.get(url=url)

            if response.ok:
                print(f"ℹ️ Downloaded {data_type} for the following game id: `{game_id}`")
                data = json.loads(response.text)

                s3.Object(bucket_name=DESTINATION_BUCKET, key=s3_key).put(
                    Body=(bytes(json.dumps(data).encode("UTF-8")))
                )
                print(f"ℹ️ Saved {data_type} into `{DESTINATION_BUCKET}` bucket successfully!")

    print("✅ Game data and shift chart downloaded successfully!")
