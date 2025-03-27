"""Game features extraction."""

from typing import List


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
