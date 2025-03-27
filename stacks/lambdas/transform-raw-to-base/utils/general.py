"""General features extraction."""


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
