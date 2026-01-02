from enum import Enum
from typing import List

import pandas as pd
from utils.general import get_general_game_features


class TeamType(Enum):
    HOME = "home"
    AWAY = "away"


class SituationType(Enum):
    FIVE_ON_FIVE = "5v5"
    FIVE_ON_FOUR = "5v4"
    FOUR_ON_FIVE = "4v5"
    OTHER = "other"

    @staticmethod
    def from_situation_code_and_team_type(situation_code: str, team_type: TeamType) -> str:
        if situation_code == "1551":
            return SituationType.FIVE_ON_FIVE.value
        elif situation_code == "1451" and team_type == TeamType.HOME:
            return SituationType.FIVE_ON_FOUR.value
        elif situation_code == "1451" and team_type == TeamType.AWAY:
            return SituationType.FOUR_ON_FIVE.value
        elif situation_code == "1541" and team_type == TeamType.HOME:
            return SituationType.FOUR_ON_FIVE.value
        elif situation_code == "1541" and team_type == TeamType.AWAY:
            return SituationType.FIVE_ON_FOUR.value
        else:
            return SituationType.OTHER.value


def get_situation_time_base(game: dict) -> List[dict]:
    """Extract situation time from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    home_team_id = game.get("homeTeam", {}).get("id")
    away_team_id = game.get("awayTeam", {}).get("id")
    situation_code_to_time = get_situation_code_to_time(game=game)

    return [
        {
            **get_general_game_features(game=game),
            "situation_team_id": team_id,
            "situation_code": situation_code,
            "situation_type": SituationType.from_situation_code_and_team_type(
                situation_code=situation_code,
                team_type=team_type,
            ),
            "situation_time": time,
        }
        for team_id, team_type in [
            (home_team_id, TeamType.HOME),
            (away_team_id, TeamType.AWAY),
        ]
        for situation_code, time in situation_code_to_time.items()
    ]


def get_situation_code_to_time(game: dict) -> dict:
    """Compute the total time spent in each game situation.

    Parameters:
    -----------
    game : dict
        A dictionary containing game data, including plays with timestamps and situation codes.

    Returns:
    --------
    dict
    """
    return (
        pd.DataFrame(
            {
                "game_id": game.get("id"),
                "type": play.get("typeDescKey"),
                "period": play.get("periodDescriptor", {}).get("number"),
                "time_in_period": play.get("timeInPeriod"),
                "situation_code": play.get("situationCode"),
            }
            for play in game.get("plays", [])
        )
        # compute time in game and categorize situations
        .assign(
            minutes_in_period=lambda _df: _df.time_in_period.str.split(":").str[0].astype(int),
            seconds_in_period=lambda _df: _df.time_in_period.str.split(":").str[1].astype(int),
            time_in_game=lambda _df: 60 * 20 * (_df.period - 1) + _df.minutes_in_period * 60 + _df.seconds_in_period,
            is_previous_situation_different=lambda _df: _df.situation_code.ne(_df.situation_code.shift()),
            situation_order_id=lambda _df: _df.is_previous_situation_different.cumsum(),
        )
        # determine the start and end time of each situation
        .groupby(["situation_order_id", "situation_code"])
        .agg(
            situation_start=("time_in_game", "min"),
            situation_end=("time_in_game", "max"),
        )
        # adjust for gaps in time between situations
        .assign(
            situation_start_correction=lambda _df: (_df.situation_start - _df.situation_end.shift()) / 2,
            situation_end_correction=lambda _df: (_df.situation_start.shift(-1) - _df.situation_end) / 2,
            situation_start=lambda _df: _df.situation_start - _df.situation_start_correction.fillna(0),
            situation_end=lambda _df: _df.situation_end + _df.situation_end_correction.fillna(0),
            time_on_ice=lambda _df: _df.situation_end - _df.situation_start,
        )
        # aggregate total time spent in each situation
        .groupby("situation_code")
        .agg(
            time_on_ice=("time_on_ice", "sum"),
        )
        .time_on_ice.to_dict()
    )
