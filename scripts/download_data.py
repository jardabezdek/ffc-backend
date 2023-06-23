"""
Script that downloads data, and organizes the downloaded files into folders structure.
"""

import io
import zipfile
from itertools import product
from pathlib import Path

import pandas as pd
import requests

DATA_SOURCE_URL = "https://moneypuck.com/moneypuck/playerData/seasonSummary"
DATA_FOLDER = Path("/usr/src/app/data/")

STAT_TYPES = ("skaters", "goalies", "teams", "lines")
SEASON_YEARS = (2018, 2019, 2020, 2021, 2022)
SEASON_PARTS = ("regular", "playoffs")


def download_statistics() -> None:
    """Download files with statistics for each statistics type, season year and season part
    (regular, or play-off) from a specified URL and save the files in the corresponding folder.

    Statistics SHOULD be available for the current season going back to the 2008/2009 season.

    Returns
    -------
        None
    """
    # create statistic type folders in the /data folder
    for stat_type in STAT_TYPES:
        stat_type_folder = DATA_FOLDER / stat_type
        Path(stat_type_folder).mkdir(parents=True, exist_ok=True)

    # download files
    for stat_type, season_year, season_part in product(STAT_TYPES, SEASON_YEARS, SEASON_PARTS):
        url = f"{DATA_SOURCE_URL}/{season_year}/{season_part}/{stat_type}.csv"
        filepath = DATA_FOLDER / stat_type / f"{season_year}_{season_part}.csv"

        if not filepath.is_file():
            df = pd.read_csv(url, storage_options={"User-Agent": "Mozilla/5.0"})
            df.to_csv(filepath, index=False)

            print(f"✅ downloaded {stat_type} data from the {season_year} {season_part} season")


def download_shots() -> None:
    """Download and extract compressed CSV files containing shots data from multiple seasons.

    The files are downloaded from a specific URL for each season and saved in the '/data/shots'
    folder. After extraction, the function renames the files by removing the "shots_" substring
    from their names.

    Returns
    -------
        None
    """
    # create /data/shots folder
    shots_folder = DATA_FOLDER / "shots"
    Path(shots_folder).mkdir(parents=True, exist_ok=True)

    # download, and extract compressed CSV files
    for season_year in SEASON_YEARS:
        url = f"https://peter-tanner.com/moneypuck/downloads/shots_{season_year}.zip"

        response = requests.get(url=url)
        with zipfile.ZipFile(io.BytesIO(response.content), "r") as file:
            file.extractall(path=shots_folder)

            print(f"✅ downloaded shots data from the {season_year} season")

    # remove "shots_" substring from files names
    for file_path in shots_folder.iterdir():
        old_file_name = file_path.name
        new_file_name = old_file_name.replace("shots_", "")
        file_path.rename(shots_folder / new_file_name)

        print(f"✅ renamed '{old_file_name}' to '{new_file_name}'")


def main():
    """Create /data folder and download data."""
    Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

    download_statistics()
    download_shots()

    print("🎉 all data downloaded successfully")


if __name__ == "__main__":
    main()
