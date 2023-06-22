"""
Script that downloads data, and organizes the downloaded files into folders structure.
"""

import datetime
from itertools import product
from pathlib import Path

import pandas as pd

DATA_SOURCE_URL = "https://moneypuck.com/moneypuck/playerData/seasonSummary"
DATA_FOLDER = Path("/usr/src/app/data/")
SEASON_PARTS = ("regular", "playoffs")
PLAYER_TYPES = ("skaters", "goalies")


def download_individual_statistics() -> None:
    """Download files with individual statistics for each season year and season part
    from a specified URL and save them in the corresponding folder.

    Returns
    -------
        None
    """
    current_year = datetime.date.today().year
    season_years = range(2018, current_year)

    # create folders in the /data folder
    for player_type in PLAYER_TYPES:
        player_type_folder = DATA_FOLDER / player_type
        Path(player_type_folder).mkdir(parents=True, exist_ok=True)

    # download files
    for player_type, season_year, season_part in product(PLAYER_TYPES, season_years, SEASON_PARTS):
        url = f"{DATA_SOURCE_URL}/{season_year}/{season_part}/{player_type}.csv"
        filepath = DATA_FOLDER / player_type / f"{season_year}_{season_part}.csv"

        if not filepath.is_file():
            df = pd.read_csv(url, storage_options={"User-Agent": "Mozilla/5.0"})
            df.to_csv(filepath, index=False)

            print(f"✅ downloaded {player_type} data from the {season_year} {season_part} season")


def main():
    """Create 'data' folder and download data."""
    Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

    download_individual_statistics()


if __name__ == "__main__":
    main()
