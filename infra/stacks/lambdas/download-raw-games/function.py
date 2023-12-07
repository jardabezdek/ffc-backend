"""
Lambda function to download a game's play-by-play and game metadata as JSON files, 
and save them into S3 bucket.
"""

import json
import os

import boto3
import requests

from utils import extract_info_from, get_yesterday_game_ids

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]
URL_GAMECENTER = "https://api-web.nhle.com/v1/gamecenter"

s3 = boto3.resource("s3")


def handler(event: dict, context):
    """Download and save a game's play-by-play and game metadata as JSON files based on the game ID.

    Parameters:
    -----------
    game_id: str
        A string representing the unique identifier of the game.

    Returns:
    --------
    None
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

                # save plays
                s3.Object(
                    bucket_name=DESTINATION_BUCKET,
                    key=f"plays/{season}/{season_type}/{game_id}.json",
                ).put(
                    Body=(
                        bytes(
                            json.dumps(
                                {
                                    "gameId": game.get("id"),
                                    "season": game.get("season"),
                                    "plays": game.get("plays"),
                                }
                            ).encode("UTF-8")
                        )
                    )
                )
                print(f"ℹ️ Saved plays into `{DESTINATION_BUCKET}` bucket successfully!")

                # save game
                s3.Object(
                    bucket_name=DESTINATION_BUCKET,
                    key=f"games/{season}/{season_type}/{game_id}.json",
                ).put(
                    Body=(
                        bytes(
                            json.dumps(
                                {key: val for key, val in game.items() if key != "plays"}
                            ).encode("UTF-8")
                        )
                    )
                )
                print(f"ℹ️ Saved game into `{DESTINATION_BUCKET}` bucket successfully!")

        return {"status_code": 200, "body": "✅ Game data downloaded successfully!"}

    return {"status_code": 500, "body": "❌ No game ids returned from NHL API."}
