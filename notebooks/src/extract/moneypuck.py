"""
Script that downloads MoneyPuck.com data, and organizes the downloaded files 
into corresponding folders.
"""

import io
import json
import zipfile
from itertools import product
from pathlib import Path

import pandas as pd
import requests

DATA_SOURCE_URL = "https://moneypuck.com/moneypuck/playerData/seasonSummary"
DATA_FOLDER = Path("/usr/src/app/data/v1/")
DATA_DICT_PATH = Path("/usr/src/app/data_dictionary.json")

STAT_TYPES = ("skaters", "goalies", "teams", "lines")
SEASON_YEARS = (2018, 2019, 2020, 2021, 2022)
SEASON_PARTS = ("regular", "playoffs")


def get_col_mappers() -> dict:
    """Return a nested dictionary where the keys represent different data types and the values are
    dictionaries that map MoneyPuck column names to corresponding new column names within each data
    type.

    Use data from the data dictionary JSON file, saved in the project root directory.

    Returns
    -------
        dict
    """
    with open(file=DATA_DICT_PATH, mode="r", encoding="utf-8") as data_dict_file:
        data_dict = json.load(data_dict_file)

    return {
        data_type: {col.get("column_moneypuck"): col.get("column") for col in cols}
        for data_type, cols in data_dict.items()
    }


def download_csv_file(
    source_filepath: str,
    destination_filepath: str,
    moneypuck_col_to_new_col: dict,
    storage_options={"User-Agent": "Mozilla/5.0"},
) -> None:
    """Download a CSV file from the specified filepath/URL address, rename the columns using
    the provided mapping dictionary, and save the modified CSV file to the specified filepath.

    Parameters
    ----------
    source_filepath : str
        The filepath, or URL from which to download the CSV file.
    moneypuck_col_to_new_col : dict
        A dictionary that maps MoneyPuck column names to new column names.
    destination_filepath : str
        The path where the modified CSV file will be saved.
    storage_options : dict
        Extra options that make sense for a particular storage connection, e.g. host, port,
        username, password, etc. For HTTP(S) URLs the key-value pairs are forwarded
        to urllib.request.Request as header options. For other URLs (e.g. starting with “s3://”,
        and “gcs://”) the key-value pairs are forwarded to fsspec.open.

    Returns
    -------
    None
        This function does not return anything directly, but saves the modified CSV file to the
        specified filepath.
    """
    return (
        pd.read_csv(source_filepath, storage_options=storage_options)
        .rename(columns=moneypuck_col_to_new_col)
        .filter(items=moneypuck_col_to_new_col.values())
        .to_csv(destination_filepath, index=False)
    )


def download_player_statistics(moneypuck_col_to_new_col: dict) -> None:
    """Download files with statistics for each statistics type, season year and season part
    from a specified URL and save the files in the corresponding folder.

    Statistics SHOULD be available for the current season going back to the 2008/2009 season.

    Parameters
    ----------
    moneypuck_col_to_new_col : dict
        A dictionary that maps MoneyPuck column names to new column names.

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
            download_csv_file(
                source_filepath=url,
                destination_filepath=filepath,
                moneypuck_col_to_new_col=moneypuck_col_to_new_col,
            )
            print(f"✅ downloaded {stat_type} data from the {season_year} {season_part} season")


def download_shots(moneypuck_col_to_new_col: dict) -> None:
    """Download and extract compressed CSV files containing shots data from multiple seasons.

    The files are downloaded from a specific URL for each season and saved in the '/data/shots'
    folder. After extraction, the function renames the files by removing the "shots_" substring
    from their names.

    Parameters
    ----------
    moneypuck_col_to_new_col : dict
        A dictionary that maps MoneyPuck column names to new column names.

    Returns
    -------
        None
    """
    # create /data/shots folder
    shots_folder = DATA_FOLDER / "shots"
    Path(shots_folder).mkdir(parents=True, exist_ok=True)

    # download, and extract compressed CSV files
    for season_year in SEASON_YEARS:
        shots_file_path = shots_folder / f"{season_year}.csv"
        if shots_file_path.exists():
            continue

        response = requests.get(
            url=f"https://peter-tanner.com/moneypuck/downloads/shots_{season_year}.zip"
        )

        with zipfile.ZipFile(io.BytesIO(response.content), "r") as file:
            file.extractall(path=shots_folder)

    # iterate over files, remove "shots_" substring from the file name, and modify CSV
    for old_file_path in shots_folder.iterdir():
        old_file_name = old_file_path.name

        if "shots_" in old_file_name:
            new_file_name = old_file_name.replace("shots_", "")
            new_file_path = old_file_path.rename(shots_folder / new_file_name)

            download_csv_file(
                source_filepath=new_file_path,
                destination_filepath=new_file_path,
                moneypuck_col_to_new_col=moneypuck_col_to_new_col,
                storage_options=None,
            )
            print(f"✅ downloaded shots data from the {season_year} season")


def download_players_lookup(moneypuck_col_to_new_col: dict) -> None:
    """Download all players lookup table and the file in the /data folder.

    Parameters
    ----------
    moneypuck_col_to_new_col : dict
        A dictionary that maps MoneyPuck column names to new column names.

    Returns
    -------
        None
    """
    url = "https://moneypuck.com/moneypuck/playerData/playerBios/allPlayersLookup.csv"
    filepath = DATA_FOLDER / "players_lookup.csv"

    if not filepath.is_file():
        download_csv_file(
            source_filepath=url,
            destination_filepath=filepath,
            moneypuck_col_to_new_col=moneypuck_col_to_new_col,
        )
        print("✅ downloaded players lookup table")


def main() -> None:
    """Create /data folder and download data.

    Returns
    -------
        None
    """
    Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

    col_mappers = get_col_mappers()

    download_player_statistics(moneypuck_col_to_new_col=col_mappers.get("players"))
    download_shots(moneypuck_col_to_new_col=col_mappers.get("shots"))
    download_players_lookup(moneypuck_col_to_new_col=col_mappers.get("players_lookup"))

    print("🎉 all data downloaded successfully")


if __name__ == "__main__":
    main()
