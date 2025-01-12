"""Script with time utils."""

import pandas as pd


def get_time_in_period_seconds(df: pd.DataFrame) -> pd.Series:
    """Convert time in period into seconds."""
    return (
        df.time_in_period.str.split(":").str[0].astype(int).mul(60) 
        + df.time_in_period.str.split(":").str[1].astype(int)
    )


def get_time_between_shots(df: pd.DataFrame) -> pd.Series:
    """Compute time between the previous and current shot."""
    return (
        df
        .groupby(by=["game_id", "period", "period_type", "event_owner_team_id"])
        .time_in_period_seconds
        .transform(lambda x: x - x.shift())
    )

def get_second(df: pd.DataFrame) -> pd.Series:
    """Compute second of a match."""
    return (
        (df.period - 1).mul(20 * 60)
        + df.time_in_period.str.split(":").str[0].astype(int).mul(60)
        + df.time_in_period.str.split(":").str[1].astype(int)
    )
