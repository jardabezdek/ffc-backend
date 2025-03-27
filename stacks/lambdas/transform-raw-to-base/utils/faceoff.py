"""Faceoff features extraction."""

from typing import List

from utils.general import get_general_event_features, get_general_game_features


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
