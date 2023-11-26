"""Script with general utils."""

from pathlib import Path

from src.config import SEASON_TYPES, SEASONS


def create_season_folders_in(data_folder: Path) -> None:
    """Create folders for each season and season type within a specified data folder.

    Parameters:
    -----------
    data_folder: Path
        The root folder where season and season type folders will be created.

    Returns:
    --------
    None
    """
    for season in SEASONS:
        for _, season_type in SEASON_TYPES:
            folder = data_folder / season[:4] / season_type
            folder.mkdir(parents=True, exist_ok=True)


def get_season_type_index(season_type: str) -> str:
    """Get the index of a season type within the SEASON_TYPES.

    Parameters:
    -----------
    season_type: str
        The season type for which the index is to be retrieved.

    Returns:
    --------
    str or None
        The index of the provided 'season_type' within the SEASON_TYPES list, or None if not found.

    """
    return {season_type: index for index, season_type in SEASON_TYPES}.get(season_type)
