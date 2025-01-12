import pandas as pd

COLS_TO_KEEP = [
    "game_id",
    "id",
    "away_team_id",
    "home_team_id",
    "period",
    "period_type",
    "time_in_period",
    "situation_code",
    "home_team_defending_side",
    "event_type",
    "sort_order",
    "x_coord",
    "y_coord",
    "x_coord_norm",
    "y_coord_norm",
    "coords_combination",
    "zone_code",
    "event_owner_team_id",
    "shot_type",
    "shooting_player_id",
    "goalie_in_net_id",
    "assist_1_player_id",
    "assist_2_player_id",
    "blocking_player_id",
    "missed_shot_reason",
    "xg",
]


def get_normalized_coordinate(df: pd.DataFrame, coord_type: str) -> pd.Series:
    def normalize_coordinate(row: dict, coord_type: str) -> int:
        home_team_defending_side = row["home_team_defending_side"]
        home_team_id = row["home_team_id"]
        event_owner_team_id = row["event_owner_team_id"]
        coord = row[f"{coord_type}_coord"]

        if (home_team_defending_side == "left" and home_team_id != event_owner_team_id) or (
            home_team_defending_side == "right" and home_team_id == event_owner_team_id
        ):
            return coord * (-1)

        return coord

    return df.apply(lambda row: normalize_coordinate(row=row, coord_type=coord_type), axis=1)


def get_combination(df: pd.DataFrame, cols: list, sep: str = ",") -> pd.Series:
    """Create a text combination of `cols`, separetad by `sep`."""
    return df.loc[:, cols].astype(str).apply(sep.join, axis=1)


def get_xg_model(df: pd.DataFrame, min_shots_cnt: int = 10) -> dict:
    """Get xG model."""
    return (
        df
        # filter out shots from team own half of the rink
        .loc[df.x_coord_norm >= 0]
        # group by coordinates combination
        .groupby(by=["coords_combination"])
        # compute shots, goals and xG values
        .agg(
            shots_cnt=("event_type", "count"),
            goals_cnt=("event_type", lambda x: x.eq("goal").sum()),
            xg=("event_type", lambda x: x.eq("goal").mean()),
        )
        # filter out rows with insignificant value
        .query(f"shots_cnt > {min_shots_cnt}")
        # save coordinates to xG value mapping
        .xg.to_dict()
    )


def model(dbt, session):
    # configure the model
    dbt.config(materialized="external")

    # get shots data
    df = dbt.ref("base_shots").df()

    # add new columns
    df["x_coord_norm"] = get_normalized_coordinate(df=df, coord_type="x")
    df["y_coord_norm"] = get_normalized_coordinate(df=df, coord_type="y")
    df["coords_combination"] = get_combination(df=df, cols=["x_coord_norm", "y_coord_norm"])

    # filter the data
    df = df.loc[
        # filter out blocked shots
        (df.event_type != "blocked-shot")
        # filter out shots from team own half of the rink
        & (df.x_coord_norm >= 0)
    ]

    # get xG model
    xg_model = get_xg_model(df=df)

    # add xG model to the data
    df["xg"] = df["coords_combination"].map(xg_model)

    # filter out columns that are not needed
    df = df.loc[:, COLS_TO_KEEP]

    return df
