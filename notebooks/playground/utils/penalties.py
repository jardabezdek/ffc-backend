"""Script with penalties utils."""

from enum import Enum

import numpy as np
import pandas as pd

REGULAR_GAME_LENGTH_SECONDS = 60 * 20 * 3
MIN_PLAYERS_ON_ICE, MAX_PLAYERS_ON_ICE = 3, 5
MAX_PLAYERS_ON_ICE_REGULAR_SEASON_OVERTIME = 3


class SeasonType(Enum):
    REGULAR = 2
    PLAYOFF = 3


def get_df_players_on_ice_per_sec(
    game_id: int, df_penalties: pd.DataFrame, df_goals: pd.DataFrame
) -> pd.DataFrame:
    """Calculate the number of players on the ice per second for a given game.

    Parameters
    ----------
    game_id : int
        The ID of the game for which to calculate the number of players on the ice.
    df_penalties : pd.DataFrame
        DataFrame containing penalty information for all games.
    df_goals : pd.DataFrame
        DataFrame containing goal information for all games.

    Returns
    -------
    pd.DataFrame
    """
    penalties = get_df_per_game(df=df_penalties, game_id=game_id)
    goals = get_df_per_game(df=df_goals, game_id=game_id)
    season_type = int(str(game_id)[5])
    game_last_second = get_game_last_second(goals=goals)

    if penalties.empty:
        home_players_in_box = np.zeros(game_last_second)
        away_players_in_box = np.zeros(game_last_second)

    else:
        penalties = adjust_penalties_end(penalties=penalties, goals=goals)
        home_players_in_box = get_players_in_box_per_sec(
            penalties=penalties.loc[penalties.event_owner_team_id == goals.home_team_id[0]],
            game_last_second=game_last_second,
        )
        away_players_in_box = get_players_in_box_per_sec(
            penalties=penalties.loc[penalties.event_owner_team_id == goals.away_team_id[0]],
            game_last_second=game_last_second,
        )

    df = pd.DataFrame(
        {
            "game_id": game_id,
            "season_type": season_type,
            "second": list(range(1, game_last_second + 1)),
            "home_players_in_box": home_players_in_box,
            "away_players_in_box": away_players_in_box,
        }
    )
    df = add_players_on_ice_per_sec(df=df)

    return df


def get_df_per_game(df: pd.DataFrame, game_id: int) -> pd.DataFrame:
    """Filter a DataFrame by game ID. Sort it.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing game data.
    game_id : int
        The ID of the game for which to filter the DataFrame.

    Returns
    -------
    pd.DataFrame
    """
    return df.loc[df.game_id == game_id].sort_values(by="sort_order").reset_index(drop=True)


def get_game_last_second(goals: pd.DataFrame) -> int:
    """Determine the last second of the game based on recorded goals.

    Parameters
    ----------
    goals : pd.DataFrame
        A DataFrame containing goal events with a 'second' column representing
        the time each goal was scored in seconds.

    Returns
    -------
    int
    """
    return max(REGULAR_GAME_LENGTH_SECONDS, goals.second.max())


def adjust_penalties_end(penalties: pd.DataFrame, goals: pd.DataFrame) -> pd.DataFrame:
    """Adjust the end times of penalties based on goals scored.

    Parameters
    ----------
    penalties : pd.DataFrame
        A DataFrame containing penalty events with 'start_second' and 'end_second'
        columns representing the start and end times of each penalty in seconds.
    goals : pd.DataFrame
        A DataFrame containing goal events with 'event_owner_team_id' and 'second'
        columns. The 'event_owner_team_id' represents the team that scored, and
        'second' represents the time of the goal in seconds.

    Returns
    -------
    pd.DataFrame
    """
    for _, goal in goals.iterrows():

        for i, penalty in penalties.iterrows():

            if (goal.event_owner_team_id != penalty.event_owner_team_id) and (
                penalty.start_second < goal.second < penalty.end_second
            ):
                penalties.at[i, "end_second"] = goal.second

                # when penalty with early finish is found, continue to another goal
                break

    return penalties


def get_players_in_box_per_sec(penalties: pd.DataFrame, game_last_second: int) -> pd.Series:
    """Compute the number of players in the penalty box for each second of the game.

    Parameters
    ----------
    penalties : pd.DataFrame
        A DataFrame containing penalty events with 'start_second' and 'end_second'
        columns. These columns represent the start and end times of each penalty in seconds.
    game_last_second : int
        The total duration of the game in seconds.

    Returns
    -------
    pd.Series
    """
    if penalties.empty:
        return np.zeros(game_last_second)

    penalties_per_sec = {}

    # iterate over all team's penalties and mark seconds in which they happened
    for i, penalty in penalties.iterrows():
        penalty_per_sec = np.zeros(game_last_second)
        penalty_per_sec[penalty.start_second : penalty.end_second] = 1
        penalties_per_sec[f"penalty_{i}"] = penalty_per_sec

    # compute number of players in box per every second
    return pd.DataFrame(data=penalties_per_sec).sum(axis=1).rename(lambda x: x + 1)


def add_players_on_ice_per_sec(df: pd.DataFrame) -> pd.DataFrame:
    """Add columns for the number of players on ice for home and away teams for each second of the game.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing game data with columns for 'season_type', 'second',
        and the number of players in the penalty box for both home and away teams.

        Expected columns:
        - 'season_type': Season type of the game (e.g., play-off or regular season).
        - 'second': The second of the game.
        - 'home_players_in_box': Number of home team players in the penalty box.
        - 'away_players_in_box': Number of away team players in the penalty box.

    Returns
    -------
    pd.DataFrame
    """
    # set default value
    df["home_players_on_ice"] = 0
    df["away_players_on_ice"] = 0

    # play-off, or regular season in regular time
    mask = (df.season_type == SeasonType.PLAYOFF.value) | (
        (df.season_type == SeasonType.REGULAR.value) & (df.second <= REGULAR_GAME_LENGTH_SECONDS)
    )
    for side in ["home", "away"]:
        df.loc[mask, f"{side}_players_on_ice"] = (
            df.loc[mask, f"{side}_players_in_box"]
            .mul(-1)
            .add(MAX_PLAYERS_ON_ICE)
            .clip(lower=MIN_PLAYERS_ON_ICE)
        )

    # regular season, over time
    mask = (df.season_type == SeasonType.REGULAR.value) & (df.second > REGULAR_GAME_LENGTH_SECONDS)
    for side in ["home", "away"]:
        other_side = "home" if side == "away" else "away"

        df.loc[mask, f"{side}_players_on_ice"] = (
            df.loc[mask, f"{other_side}_players_in_box"]
            .add(MAX_PLAYERS_ON_ICE_REGULAR_SEASON_OVERTIME)
            .clip(upper=MAX_PLAYERS_ON_ICE)
        )

    return df


def get_strength(df: pd.DataFrame) -> np.array:
    """Compute the strength of the game.

    The strength is represented as a string indicating the number of players on ice for the away
    team versus the number of players on ice for the home team. The representation is adjusted
    depending on whether the event owner team is the away or home team.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing columns for the event owner team, home team, and away team
        players on ice.

    Returns
    -------
    np.array
    """
    return np.where(
        df.event_owner_team_id == df.away_team_id,
        (
            df.away_players_on_ice.astype(int).astype(str)
            + "v"
            + df.home_players_on_ice.astype(int).astype(str)
        ),
        (
            df.home_players_on_ice.astype(int).astype(str)
            + "v"
            + df.away_players_on_ice.astype(int).astype(str)
        ),
    )
