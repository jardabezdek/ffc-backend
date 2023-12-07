"""Script that downloads games info."""

import itertools
import json

import requests

from src.config import FOLDER_DATA_GAMES, FOLDER_DATA_PLAYS, SEASONS, URL_GAMECENTER
from src.utils.games import (
    extract_info_from,
    get_playoff_games_ids,
    get_regular_season_games_ids,
)
from src.utils.general import create_season_folders_in


def download_season_games(regular=True, playoffs=False) -> None:
    """Download and store game data for regular season and/or playoff games for all seasons.

    Parameters:
    -----------
    regular: bool, optional
        If True, download data for regular season games. Default is True.
    playoffs: bool, optional
        If True, download data for playoff games. Default is False.

    Returns:
    --------
    None
    """
    for season in SEASONS:
        season_first_year = int(season[:4])

        for game_id in itertools.chain(
            get_regular_season_games_ids(season=season_first_year) if regular else [],
            get_playoff_games_ids(season=season_first_year) if playoffs else [],
        ):
            download_game(game_id=game_id)

        print(f"✅ {season} season loaded successfully!")


def download_game(game_id: str) -> None:
    """Download and save a game's play-by-play and game metadata as JSON files based on the game ID.

    Parameters:
    -----------
    game_id: str
        A string representing the unique identifier of the game.

    Returns:
    --------
    None
    """
    season, season_type = extract_info_from(game_id=game_id)
    file_path_game = FOLDER_DATA_GAMES / season / season_type / f"{game_id}.json"
    file_path_plays = FOLDER_DATA_PLAYS / season / season_type / f"{game_id}.json"

    if file_path_game.exists() and file_path_plays.exists():
        print(f"ℹ️ Info: Game {game_id} was already downloaded!")

    else:
        response = requests.get(url=f"{URL_GAMECENTER}/{game_id}/play-by-play")

        if response.ok:
            game = json.loads(response.text)

            # if game is finished, save data
            if game.get("gameState") == "OFF":
                # save plays
                with open(file_path_plays, mode="w", encoding="utf-8") as file:
                    json.dump(
                        obj={
                            "gameId": game.get("id"),
                            "season": game.get("season"),
                            "plays": game.get("plays"),
                        },
                        fp=file,
                    )

                # save game
                with open(file_path_game, mode="w", encoding="utf-8") as file:
                    json.dump(
                        obj={key: val for key, val in game.items() if key != "plays"},
                        fp=file,
                    )

        else:
            print(f"❌ Error: Game {game_id} was NOT loaded!")


def main() -> None:
    """Download games data.

    Returns
    -------
        None
    """
    create_season_folders_in(data_folder=FOLDER_DATA_GAMES)
    create_season_folders_in(data_folder=FOLDER_DATA_PLAYS)

    download_season_games(regular=True, playoffs=True)

    print("🎉 All games data downloaded successfully!")


if __name__ == "__main__":
    main()
