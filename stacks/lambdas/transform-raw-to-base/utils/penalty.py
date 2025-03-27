"""Penalty features extraction."""

from typing import List

from utils.general import get_general_event_features, get_general_game_features


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
