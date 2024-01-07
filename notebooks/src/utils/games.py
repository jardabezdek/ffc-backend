"""Script with games utils."""

import itertools
from typing import List, Tuple

from src.config import SEASON_TYPES
from src.utils.general import get_season_type_index


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
    season_type = dict(SEASON_TYPES).get(game_id[4:6])
    return season, season_type


def get_regular_season_games_ids(season: int) -> List[str]:
    """Get game IDs for regular season games in a specified season.

    Parameters:
    -----------
    season: int
        The starting year of the season for which regular season game IDs are to be retrieved.

    Returns:
    --------
    List[str]
        A list containing game IDs representing regular season games for the specified season.
    """
    season_type_i = get_season_type_index(season_type="regular")

    if season >= 2021:
        games_cnt = 1312
    elif season == 2020:
        games_cnt = 868
    elif season == 2019:
        games_cnt = 1082
    elif season == 2018:
        games_cnt = 1272
    elif season == 2017:
        games_cnt = 1271
    else:
        games_cnt = 1230

    return [
        f"{season}{season_type_i}{str(game_i).rjust(4, '0')}" for game_i in range(1, games_cnt + 1)
    ]


def get_playoff_games_ids(season: int) -> List[str]:
    """Get game IDs for playoff games in a specified season.

    Parameters:
    -----------
    season: int
        The starting year of the season for which playoff game IDs are to be retrieved.

    Returns:
    --------
    List[str]
        A list containing game IDs representing playoff games for the specified season.
    """
    season_type_i = get_season_type_index(season_type="playoffs")
    prefixes = itertools.chain(
        [f"{season}{season_type_i}01{match_up_i}" for match_up_i in range(1, 9)],
        [f"{season}{season_type_i}02{match_up_i}" for match_up_i in range(1, 5)],
        [f"{season}{season_type_i}03{match_up_i}" for match_up_i in range(1, 3)],
        [f"{season}{season_type_i}041"],
    )
    return [
        f"{prefix}{game_i}" for prefix, game_i in itertools.product(prefixes, list(range(1, 8)))
    ]
