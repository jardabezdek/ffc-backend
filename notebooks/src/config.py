"""Config for scripts in src/ folder."""

from pathlib import Path

FOLDER_DATA = Path("/usr/src/app/data/")
FOLDER_DATA_TEAMS = Path("/usr/src/app/data/teams/")
FOLDER_DATA_PLAYERS = Path("/usr/src/app/data/players/")
FOLDER_DATA_GAMES = Path("/usr/src/app/data/games/")
FOLDER_DATA_PLAYS = Path("/usr/src/app/data/plays/")

FILE_TEAM_ABBREV_TO_TEAM = FOLDER_DATA_TEAMS / "team_abbrev_to_team.json"
FILE_PLAYERS = FOLDER_DATA_PLAYERS / "players.csv"

SEASONS = (
    "20152016",
    "20162017",
    "20172018",
    "20182019",
    "20192020",
    "20202021",
    "20212022",
    "20222023",
    "20232024",
)
SEASON_TYPES = (
    ("01", "preseason"),
    ("02", "regular"),
    ("03", "playoffs"),
    ("04", "all-star"),
)

URL_STANDINGS = "https://api-web.nhle.com/v1/standings"
URL_ROSTER = "https://api-web.nhle.com/v1/roster"
URL_GAMECENTER = "https://api-web.nhle.com/v1/gamecenter"
