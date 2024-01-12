"""Util functions for lambda function."""

import datetime
import json
from enum import Enum
from typing import List, Tuple

import requests

URL_SCHEDULE = "https://api-web.nhle.com/v1/schedule"


class SeasonType(Enum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFF = 3
    ALLSTAR = 4


def get_yesterday_date(date_format="%Y-%m-%d") -> str:
    """Get yesterday's date in a specified format.

    Parameters:
    -----------
    date_format : str, optional
        The format in which the date will be returned. Defaults to "%Y-%m-%d".

    Returns:
    --------
    str
        A string representing yesterday's date in the specified format.
    """
    yesterday_datetime = datetime.datetime.now() - datetime.timedelta(days=1)
    return yesterday_datetime.strftime(format=date_format)


def get_yesterday_game_ids() -> List[str]:
    """Get IDs of finished games played yesterday.

    Returns:
    --------
    list
        A list containing IDs of finished games played yesterday.
    """
    yesterday_date_str = get_yesterday_date()
    response = requests.get(url=f"{URL_SCHEDULE}/{yesterday_date_str}")

    if response.ok:
        schedule = json.loads(response.text)

        for game_day in schedule.get("gameWeek"):
            if game_day.get("date") == yesterday_date_str:
                return [
                    str(game.get("id"))
                    for game in game_day.get("games")
                    if game.get("gameState") == "OFF"
                ]
    return []


def extract_info_from(game_id: str) -> Tuple[str, str]:
    """Extract season and season type information from a game ID.

    Parameters:
    -----------
    game_id : str
        A string representing the unique identifier of a game.

    Returns:
    --------
    Tuple[str, str]
        A tuple containing information about the season and season type extracted
        from the provided game ID.
    """
    season = game_id[:4]

    season_type_val = int(game_id[5])
    season_type = SeasonType(season_type_val).name.lower()

    return season, season_type
