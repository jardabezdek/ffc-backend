"""
Lambda function that
- reads JSON file with raw game data,
- extracts base info about game, and events,
- saves base data into PARQUET files.
"""

import json
import os
from typing import Any

import boto3
import pandas as pd
from utils import (
    extract_info_from,
    get_faceoff_base,
    get_game_base,
    get_hit_base,
    get_penalty_base,
    get_player_base,
    get_possession_change_base,
    get_shot_base,
    get_situation_time_base,
)

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]

s3 = boto3.resource("s3")


def handler(event: dict, context: Any) -> None:
    """Read JSON file with raw game data, extract base info, and save data into PARQUET files.

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
        input_file_bucket = event.get("Records")[0].get("s3").get("bucket").get("name")
        input_file_key = event.get("Records")[0].get("s3").get("object").get("key")
        game_id, season, season_type = extract_info_from(key=input_file_key)

        game = json.loads(
            s3.Object(bucket_name=input_file_bucket, key=input_file_key).get()["Body"].read().decode("utf-8")
        )
        print(f"ℹ️ Loaded game data from `{input_file_bucket}/{input_file_key}`")

        # save base data
        for folder_name, fn in (
            ("games", get_game_base),
            ("shots", get_shot_base),
            ("faceoffs", get_faceoff_base),
            ("hits", get_hit_base),
            ("possession-changes", get_possession_change_base),
            ("penalties", get_penalty_base),
            ("players", get_player_base),
            ("situation-time", get_situation_time_base),
        ):
            base = fn(game=game)
            key = f"{folder_name}/{season}/{season_type}/{game_id}.parquet"

            if base:
                pd.DataFrame(base).to_parquet(path=f"s3://{DESTINATION_BUCKET}/{key}", index=False)
                print(f"ℹ️ Saved `{DESTINATION_BUCKET}/{key}` successfully!")

        print("✅ Raw data transformed into base successfully!")

    except Exception as exc:
        print(f"❌ Internal server error: {exc}")
