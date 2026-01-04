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
    GameInfo,
    extract_info_from,
    get_faceoff_base,
    get_game_base,
    get_hit_base,
    get_penalty_base,
    get_player_base,
    get_possession_change_base,
    get_shift_base,
    get_shot_base,
    get_situation_time_base,
)

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]

s3 = boto3.resource("s3")


def load_s3_object_to_dict(bucket_name: str, key: str) -> dict:
    """Load S3 object to dictionary.

    Parameters:
    -----------
    bucket_name: str
        A string that contains the name of the bucket to load the S3 object from.
    key: str
        A string that contains the key of the S3 object to load.

    Returns:
    --------
    dict
        A dictionary that contains the contents of the S3 object.
    """
    return json.loads(s3.Object(bucket_name=bucket_name, key=key).get()["Body"].read().decode("utf-8"))


def save_base_data(base: list, folder_name: str, game_info: GameInfo) -> None:
    """Save base data.

    Parameters:
    -----------
    base: list
        A list of dictionaries that contains the base data.
    folder_name: str
        A string that contains the name of the folder to save the base data.
    game_info: GameInfo
        A GameInfo object that contains the game information.

    Returns:
    --------
    None
    """
    key = f"{folder_name}/{game_info.season}/{game_info.season_type}/{game_info.game_id}.parquet"

    if base:
        pd.DataFrame(base).to_parquet(path=f"s3://{DESTINATION_BUCKET}/{key}", index=False)
        print(f"ℹ️ Saved `{DESTINATION_BUCKET}/{key}` successfully!")


def process_game_data(bucket_name: str, key: str, game_info: GameInfo) -> None:
    """Process game data.

    Parameters:
    -----------
    bucket_name: str
        A string that contains the name of the bucket to load the S3 object from.
    key: str
        A string that contains the key of the S3 object to load.
    game_info: GameInfo
        A GameInfo object that contains the game information.

    Returns:
    --------
    None
    """
    game = load_s3_object_to_dict(bucket_name=bucket_name, key=key)
    print(f"ℹ️ Loaded raw data from `{bucket_name}/{key}`")

    # save base data
    for folder_name, fn in [
        ("games", get_game_base),
        ("shots", get_shot_base),
        ("faceoffs", get_faceoff_base),
        ("hits", get_hit_base),
        ("possession-changes", get_possession_change_base),
        ("penalties", get_penalty_base),
        ("players", get_player_base),
        ("situation-time", get_situation_time_base),
    ]:
        base = fn(game=game)
        save_base_data(base=base, folder_name=folder_name, game_info=game_info)


def process_shift_chart_data(bucket_name: str, key: str, game_info: GameInfo) -> None:
    """Process shift chart data.

    Parameters:
    -----------
    bucket_name: str
        A string that contains the name of the bucket to load the S3 object from.
    key: str
        A string that contains the key of the S3 object to load.
    game_info: GameInfo
        A GameInfo object that contains the game information.

    Returns:
    --------
    None
    """
    shift_chart = load_s3_object_to_dict(bucket_name=bucket_name, key=key)
    print(f"ℹ️ Loaded raw data from `{bucket_name}/{key}`")

    # save base data
    for folder_name, fn in [
        ("shifts", get_shift_base),
    ]:
        base = fn(shift_chart=shift_chart)
        save_base_data(base=base, folder_name=folder_name, game_info=game_info)


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
        game_info = extract_info_from(key=input_file_key)

        if input_file_key.startswith("games/"):
            process_game_data(bucket_name=input_file_bucket, key=input_file_key, game_info=game_info)
        elif input_file_key.startswith("shift-charts/"):
            process_shift_chart_data(bucket_name=input_file_bucket, key=input_file_key, game_info=game_info)
        else:
            print(f"❌ Invalid file key: {input_file_key}")
            return

        print("✅ Raw data transformed into base successfully!")

    except Exception as exc:
        print(f"❌ Internal server error: {exc}")
