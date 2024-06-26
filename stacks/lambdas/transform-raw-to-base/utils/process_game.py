"""Util functions for lambda function."""

from enum import Enum
from pathlib import Path
from typing import List, Tuple

import requests


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


def get_game_base(game: dict) -> List[dict]:
    """Extract game details from a dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing raw game information.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            "id": game.get("id"),
            "season": game.get("season"),
            "type": game.get("gameType"),
            "date": game.get("gameDate"),
            "start_time_utc": game.get("startTimeUTC"),
            "venue": game.get("venue", {}).get("default"),
            "period": game.get("periodDescriptor", {}).get("number"),
            "period_type": game.get("periodDescriptor", {}).get("periodType"),
            "away_team_id": game.get("awayTeam", {}).get("id"),
            "away_team_abbrev": game.get("awayTeam", {}).get("abbrev"),
            "away_team_score": game.get("awayTeam", {}).get("score"),
            # "away_team_sog": game.get("awayTeam", {}).get("sog"),
            # "away_team_logo_url": game.get("awayTeam", {}).get("logo"),
            "home_team_id": game.get("homeTeam", {}).get("id"),
            "home_team_abbrev": game.get("homeTeam", {}).get("abbrev"),
            "home_team_score": game.get("homeTeam", {}).get("score"),
            # "home_team_sog": game.get("homeTeam", {}).get("sog"),
            # "home_team_logo_url": game.get("homeTeam", {}).get("logo"),
        }
    ]


def get_general_game_features(game: dict) -> dict:
    """Extract general features from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing raw game information.

    Returns:
    --------
    dict
    """
    return {
        "game_id": game.get("id"),
        "game_date": game.get("gameDate"),
        "away_team_id": game.get("awayTeam", {}).get("id"),
        "home_team_id": game.get("homeTeam", {}).get("id"),
    }


def get_general_event_features(event: dict) -> dict:
    """Extract general features from an event dictionary.

    Parameters:
    -----------
    event : dict
        A dictionary containing event information.

    Returns:
    --------
    dict
    """
    return {
        "id": event.get("eventId"),
        "period": event.get("periodDescriptor", {}).get("number"),
        "period_type": event.get("periodDescriptor", {}).get("periodType"),
        "time_in_period": event.get("timeInPeriod"),
        "time_remaining": event.get("timeRemaining"),
        "situation_code": event.get("situationCode"),
        "home_team_defending_side": event.get("homeTeamDefendingSide"),
        # "type_code": event.get("typeCode"),
        "event_type": event.get("typeDescKey"),
        "sort_order": event.get("sortOrder"),
        "x_coord": event.get("details", {}).get("xCoord"),
        "y_coord": event.get("details", {}).get("yCoord"),
        "zone_code": event.get("details", {}).get("zoneCode"),
        "event_owner_team_id": event.get("details", {}).get("eventOwnerTeamId"),
    }


def get_shot_base(game: dict) -> List[dict]:
    """Extract shots and goals from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            **get_general_game_features(game=game),
            **get_general_event_features(event=event),
            "shot_type": event.get("details", {}).get("shotType"),
            "shooting_player_id": (
                event.get("details", {}).get("scoringPlayerId")
                if event.get("typeDescKey") == "goal"
                else event.get("details", {}).get("shootingPlayerId")
            ),
            "goalie_in_net_id": event.get("details", {}).get("goalieInNetId"),
            "assist_1_player_id": event.get("details", {}).get("assist1PlayerId"),
            "assist_2_player_id": event.get("details", {}).get("assist2PlayerId"),
            "blocking_player_id": event.get("details", {}).get("blockingPlayerId"),
            "missed_shot_reason": event.get("details", {}).get("reason"),
        }
        for event in game.get("plays")
        if event.get("typeDescKey") in ("goal", "shot-on-goal", "blocked-shot", "missed-shot")
    ]


def get_faceoff_base(game: dict) -> List[dict]:
    """Extract face-offs from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            **get_general_game_features(game=game),
            **get_general_event_features(event=event),
            "winning_player_id": event.get("details", {}).get("winningPlayerId"),
            "losing_player_id": event.get("details", {}).get("losingPlayerId"),
        }
        for event in game.get("plays")
        if event.get("typeDescKey") in ("faceoff")
    ]


def get_hit_base(game: dict) -> List[dict]:
    """Extract hits from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            **get_general_game_features(game=game),
            **get_general_event_features(event=event),
            "hitting_player_id": event.get("details", {}).get("hittingPlayerId"),
            "hittee_player_id": event.get("details", {}).get("hitteePlayerId"),
        }
        for event in game.get("plays")
        if event.get("typeDescKey") in ("hit")
    ]


def get_possession_change_base(game: dict) -> List[dict]:
    """Extract takeaways and giveaways from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            **get_general_game_features(game=game),
            **get_general_event_features(event=event),
            "player_id": event.get("details", {}).get("playerId"),
        }
        for event in game.get("plays")
        if event.get("typeDescKey") in ("takeaway", "giveaway")
    ]


def get_penalty_base(game: dict) -> List[dict]:
    """Extract penalties from a game dictionary.

    Parameters:
    -----------
    game : dict
        A dictionary containing game information.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            **get_general_game_features(game=game),
            **get_general_event_features(event=event),
            "penalty_code": event.get("details", {}).get("typeCode"),
            "penalty_type": event.get("details", {}).get("descKey"),
            "duration": event.get("details", {}).get("duration"),
            "committed_by_player_id": event.get("details", {}).get("committedByPlayerId"),
            "drawn_by_player_id": event.get("details", {}).get("drawnByPlayerId"),
            "served_by_player_id": event.get("details", {}).get("servedByPlayerId"),
        }
        for event in game.get("plays")
        if event.get("typeDescKey") in ("penalty")
    ]


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
    response = requests.get(
        url=f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season}/{season_type}"
    )

    game_log = {}

    if response.ok:
        game_log = next(
            (item for item in response.json().get("gameLog", {}) if item["gameId"] == game_id), {}
        )

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
