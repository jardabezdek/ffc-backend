import pandas as pd

COLS_TO_KEEP = [
    "game_id",
    "season",
    "season_type",
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
    "is_fenwick",
    "is_from_own_half",
]


def model(dbt, session):
    # configure the model
    dbt.config(materialized="external")

    # get shots data
    df = dbt.ref("base_shots").df()

    # add new columns
    df["season"] = df.game_id.astype(str).str[:4].astype(int)
    df["season_type"] = df.game_id.astype(str).str[5].astype(int)
    df["x_coord_norm"] = get_normalized_coordinate(df=df, coord_type="x")
    df["y_coord_norm"] = get_normalized_coordinate(df=df, coord_type="y")
    df["coords_combination"] = get_combination(df=df, cols=["x_coord_norm", "y_coord_norm"])
    df["is_fenwick"] = df.event_type != "blocked-shot"
    df["is_from_own_half"] = df.x_coord_norm >= 0

    # add xG column
    xg_model = get_xg_model(df=df)
    xg_filter = (df.is_fenwick) & (df.is_from_own_half)
    df.loc[xg_filter, "xg"] = df.loc[xg_filter, "coords_combination"].map(xg_model)

    # filter out columns that are not needed
    df = df.loc[:, COLS_TO_KEEP]

    return df


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
        # apply filters
        .loc[(df.is_fenwick) & (df.is_from_own_half)]
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
