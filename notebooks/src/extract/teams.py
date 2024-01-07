"""Script that downloads teams info."""

import json
from pathlib import Path

import pandas as pd
import requests

from src.config import FILE_TEAM_ABBREV_TO_TEAM, FOLDER_DATA_TEAMS, URL_STANDINGS


def get_current_standings() -> dict:
    """Retrieve the current standings.

    Returns:
    --------
    dict or None
        A dictionary containing the current standings information if the request is successful.
        Returns None if there are issues in retrieving the standings data.
    """
    response = requests.get(url=f"{URL_STANDINGS}/now")

    if response.ok:
        standings = json.loads(response.text).get("standings")
        print("✅ Standings loaded successfully!")

    else:
        print("❌ Error: Standings were NOT loaded!")

    return standings


def download_team_abbrev_to_team_mapping(standings: dict) -> None:
    """Download and store team abbreviation to team name mapping as a JSON file.

    Parameters:
    -----------
    standings : dict
        A dictionary containing the current standings information.

    Returns:
    --------
    None
    """
    team_abbrev_to_team = (
        pd.DataFrame(
            [
                {
                    "team": standing.get("teamName").get("default"),
                    "team_abbrev": standing.get("teamAbbrev").get("default"),
                    "conference": standing.get("conferenceAbbrev"),
                }
                for standing in standings
            ]
        )
        .sort_values(by=["conference", "team"])
        .set_index("team_abbrev")
        .team.to_dict()
    )

    with open(FILE_TEAM_ABBREV_TO_TEAM, mode="w", encoding="utf-8") as file:
        json.dump(obj=team_abbrev_to_team, fp=file)


def read_team_abbrev_to_team_mapping() -> dict:
    """Read team abbreviation to team name mapping from a JSON file.

    Returns:
    --------
    dict
        A dictionary containing the team abbreviation to team name mapping.
    """
    with open(FILE_TEAM_ABBREV_TO_TEAM, mode="r", encoding="utf-8") as file:
        team_abbrev_to_team = json.load(file)

    return team_abbrev_to_team


def main() -> None:
    """Download teams data.

    Returns
    -------
        None
    """
    standings = get_current_standings()

    FOLDER_DATA_TEAMS.mkdir(parents=True, exist_ok=True)
    download_team_abbrev_to_team_mapping(standings=standings)

    print("🎉 All teams data downloaded successfully!")


if __name__ == "__main__":
    main()
