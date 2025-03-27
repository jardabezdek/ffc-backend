"""Player features extraction."""

from typing import List

import requests
from utils.general import get_general_game_features


def get_player_base(game: dict) -> List[dict]:
    """Extract players from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    game_id = game.get("id")
    season_start_year = int(game_id / 1e6)

    return [
        {
            **get_general_game_features(game=game),
            "player_id": player.get("playerId"),
            "team_id": player.get("teamId"),
            "season": game.get("season"),
            "first_name": player.get("firstName", {}).get("default"),
            "last_name": player.get("lastName", {}).get("default"),
            "sweater_number": player.get("sweaterNumber"),
            "position_code": player.get("positionCode"),
            "headshot": player.get("headshot"),
            **get_game_log_features(
                player_id=player.get("playerId"),
                game_id=game.get("id"),
                season=f"{season_start_year}{season_start_year + 1}",
                season_type=str(game_id)[5],
            ),
        }
        for player in game.get("rosterSpots")
    ]


def get_game_log_features(player_id: int, game_id: int, season: str, season_type: str) -> dict:
    """
    Fetch and extract game log features for a specified player and game.

    Parameters
    ----------
    player_id : int
        The unique identifier for the player.
    game_id : int
        The unique identifier for the game.
    season : str
        The season in the format 'YYYYYYYY' (e.g., '20202021').
    season_type : str
        The type of the season ('2' for regular, '3' for playoffs).

    Returns
    -------
    dict
    """
    response = requests.get(url=f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season}/{season_type}")

    game_log = {}

    if response.ok:
        game_log = next((item for item in response.json().get("gameLog", {}) if item["gameId"] == game_id), {})

    return {
        "goals": game_log.get("goals"),
        "assists": game_log.get("assists"),
        "points": game_log.get("points"),
        "pim": game_log.get("pim"),
        "toi": game_log.get("toi"),
        # goaltender stats
        "games_started": game_log.get("gamesStarted"),
        "shots_against": game_log.get("shotsAgainst"),
        "goals_against": game_log.get("goalsAgainst"),
        "save_pctg": game_log.get("savePctg"),
        "shutouts": game_log.get("shutouts"),
        # skater stats
        "plus_minus": game_log.get("plusMinus"),
        "power_play_goals": game_log.get("powerPlayGoals"),
        "power_play_points": game_log.get("powerPlayPoints"),
        "game_winning_goals": game_log.get("gameWinningGoals"),
        "ot_goals": game_log.get("otGoals"),
        "shots": game_log.get("shots"),
        "shifts": game_log.get("shifts"),
        "shorthanded_goals": game_log.get("shorthandedGoals"),
        "shorthanded_points": game_log.get("shorthandedPoints"),
    }
