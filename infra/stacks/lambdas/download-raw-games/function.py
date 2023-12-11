"""
Lambda function to download a game's play-by-play and game metadata as JSON files, 
and save them into S3 bucket.
"""

import json
import os
from typing import Any

import boto3
import requests

from utils import extract_info_from, get_yesterday_game_ids

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]
URL_GAMECENTER = "https://api-web.nhle.com/v1/gamecenter"

s3 = boto3.resource("s3")


def handler(event: dict, context: Any) -> dict:
    """Download and save a game data as JSON file based on the game ID.

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
    yesterday_game_ids = get_yesterday_game_ids()

    if yesterday_game_ids:
        for game_id in yesterday_game_ids:
            season, season_type = extract_info_from(game_id=game_id)

            # call NHL API
            response = requests.get(url=f"{URL_GAMECENTER}/{game_id}/play-by-play")

            if response.ok:
                print(f"ℹ️ Downloaded game data for the following game id: `{game_id}`")
                game = json.loads(response.text)

                # save game
                s3.Object(
                    bucket_name=DESTINATION_BUCKET,
                    key=f"games/{season}/{season_type}/{game_id}.json",
                ).put(Body=(bytes(json.dumps(game).encode("UTF-8"))))
                print(f"ℹ️ Saved game into `{DESTINATION_BUCKET}` bucket successfully!")

        return {"status_code": 200, "body": "✅ Game data downloaded successfully!"}

    return {"status_code": 500, "body": "❌ No game ids returned from NHL API."}
