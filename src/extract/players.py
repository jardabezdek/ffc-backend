"""Script that downloads players info."""

import itertools
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd
import requests

from src.config import FILE_PLAYERS, FOLDER_DATA_PLAYERS, SEASONS, URL_ROSTER
from src.extract.teams import read_team_abbrev_to_team_mapping


def get_season_rosters() -> List:
    """Retrieve season rosters for teams and compile player information.

    Returns:
    --------
    list
        A list containing player information from the season rosters of various teams.

    """
    rosters = []
    team_abbrev_to_team = read_team_abbrev_to_team_mapping()

    for team in team_abbrev_to_team.keys():
        for season in SEASONS:
            url = f"{URL_ROSTER}/{team}/{season}"
            response = requests.get(url)

            if response.ok:
                roster = json.loads(response.text)

            else:
                print(f"❌ Error: Roster for {team} {season} was NOT loaded!")
                continue

            rosters += [
                {
                    "id": player.get("id"),
                    "first_name": player.get("firstName", {}).get("default"),
                    "last_name": player.get("lastName", {}).get("default"),
                    "position": player.get("positionCode"),
                    "shoots_catches": player.get("shootsCatches"),
                    "height_cm": player.get("heightInCentimeters"),
                    "weight_kg": player.get("weightInKilograms"),
                    "birth_date": player.get("birthDate"),
                    "birth_city": player.get("birthCity", {}).get("default"),
                    "birth_country": player.get("birthCountry"),
                    "birth_state_province": player.get("birthStateProvince", {}).get("default"),
                    "last_active_team": team,
                    "last_active_season": season,
                    "url_headshot": player.get("headshot"),
                }
                for player in itertools.chain(
                    roster.get("forwards"),
                    roster.get("defensemen"),
                    roster.get("goalies"),
                )
            ]

        print(f"✅ {team} roster loaded successfully!")

    return rosters


def download_players_data(rosters: List[Dict]) -> None:
    """
    Download and store player data to a CSV file.

    Parameters:
    -----------
    rosters : List[Dict]
        A list of dictionaries containing player information, retrieved from season rosters.

    Returns:
    --------
    None
    """
    (
        pd.DataFrame(rosters)
        .sort_values(by=["id", "last_active_season"])
        .drop_duplicates(subset="id", keep="last")
        .reset_index(drop=True)
        .to_csv(FILE_PLAYERS, index=False)
    )


def read_players_data() -> pd.DataFrame:
    """Read players data from a CSV file.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the players data.
    """
    return pd.read_csv(FILE_PLAYERS)


def main() -> None:
    """Download players data.

    Returns
    -------
        None
    """
    rosters = get_season_rosters()

    FOLDER_DATA_PLAYERS.mkdir(parents=True, exist_ok=True)
    download_players_data(rosters=rosters)

    print("🎉 All players data downloaded successfully!")


if __name__ == "__main__":
    main()
