"""Possession change features extraction."""

from typing import List

from utils.general import get_general_event_features, get_general_game_features


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
