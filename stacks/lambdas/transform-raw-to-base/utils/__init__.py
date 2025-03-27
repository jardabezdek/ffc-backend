from enum import Enum
from pathlib import Path
from typing import Tuple

from utils.faceoff import get_faceoff_base
from utils.game import get_game_base
from utils.hit import get_hit_base
from utils.penalty import get_penalty_base
from utils.player import get_player_base
from utils.possession_change import get_possession_change_base
from utils.shot import get_shot_base
from utils.situation_time import get_situation_time_base


class SeasonType(Enum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFF = 3
    ALLSTAR = 4


def extract_info_from(key: str) -> Tuple[str, str, str]:
    """Extract game_id, season, and season type from a key.

    Parameters:
    -----------
    key : str
        A string representing the unique identifier S3 bucket file.

    Returns:
    --------
    Tuple[str, str, str]
        A tuple containing information about the game_id, season, and season type extracted
        from the provided key.
    """
    game_id = Path(key).stem

    season = game_id[:4]

    season_type_val = int(game_id[5])
    season_type = SeasonType(season_type_val).name.lower()

    return game_id, season, season_type


__all__ = [
    "extract_info_from",
    "get_faceoff_base",
    "get_game_base",
    "get_hit_base",
    "get_penalty_base",
    "get_player_base",
    "get_possession_change_base",
    "get_shot_base",
    "get_situation_time_base",
]
