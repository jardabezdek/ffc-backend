"""Shot features extraction."""

from typing import List

from utils.general import get_general_event_features, get_general_game_features


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
