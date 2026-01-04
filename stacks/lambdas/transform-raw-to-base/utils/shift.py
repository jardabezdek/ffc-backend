from typing import List


def get_shift_base(shift_chart: dict) -> List[dict]:
    """Extract shift data from a shift chart dictionary.

    Parameters:
    -----------
    shift_chart : dict
        A dictionary containing shift chart data.

    Returns:
    --------
    List[dict]
    """
    return [
        {
            "game_id": shift.get("gameId"),
            "shift_id": shift.get("id"),
            "player_id": shift.get("playerId"),
            "team_id": shift.get("teamId"),
            "period": shift.get("period"),
            "start_time": shift.get("startTime"),
            "end_time": shift.get("endTime"),
            "duration": shift.get("duration"),
            "shift_number": shift.get("shiftNumber"),
        }
        for shift in shift_chart.get("data")
    ]
