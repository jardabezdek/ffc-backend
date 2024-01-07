"""Utils funtion for stremlit app styling."""

from pathlib import Path

import pandas as pd
import streamlit as st
import toml

PAGES_CONFIG_PATH = Path(__file__).resolve().parent.parent / ".streamlit" / "pages.toml"
STANDDINGS_DF_COLUMN_CONFIG = {
    "rank": st.column_config.NumberColumn(
        label="Rank",
        help="Rank",
    ),
    "team_logo_url": st.column_config.ImageColumn(
        label="Team",
        width="small",
    ),
    "team_full_name": st.column_config.TextColumn(
        label=" ",
        # width="medium",
    ),
    "games_played": st.column_config.NumberColumn(
        label="GP",
        help="Games played",
    ),
    "wins": st.column_config.NumberColumn(
        label="W",
        help="Wins (worth two points)",
    ),
    "losses": st.column_config.NumberColumn(
        label="L",
        help="Losses (worth zero points)",
    ),
    "ots": st.column_config.NumberColumn(
        label="OT",
        help="OT/Shootout losses (worth one point)",
    ),
    "points": st.column_config.NumberColumn(
        label="PTS",
        help="Points",
    ),
    "points_pct": st.column_config.NumberColumn(
        label="P%",
        help="Points Percentage",
        format="%0.3f",
    ),
    "wins_reg": st.column_config.NumberColumn(
        label="RW",
        help="Regulation Wins",
    ),
    "wins_ot": st.column_config.NumberColumn(
        label="ROW",
        help="Regulation plus Overtime Wins",
    ),
    "goals_for": st.column_config.NumberColumn(
        label="GF",
        help="Goals For",
    ),
    "goals_against": st.column_config.NumberColumn(
        label="GA",
        help="Goals Against",
    ),
    "goals_diff": st.column_config.NumberColumn(
        label="DIFF",
        help="Goal Differential",
    ),
    "record_home": st.column_config.TextColumn(
        label="HOME",
        help="Home Record",
    ),
    "record_away": st.column_config.TextColumn(
        label="AWAY",
        help="Away Record",
    ),
    "record_so": st.column_config.TextColumn(
        label="S/O",
        help="Record in games decided by Shootout",
    ),
    "record_last_10": st.column_config.TextColumn(
        label="L10",
        help="Record in last ten games",
    ),
}


def style_page(file_path: Path) -> None:
    """Style a page based on the provided file path.

    Parameters:
    -----------
    file_path : Path
        The path to the file corresponding to the Streamlit page.

    Notes:
    ------
    This function loads a configuration file containing details about different pages
    and their respective configurations. It fetches the configuration for the provided
    file path and uses it to set the page title, icon, and layout using Streamlit's
    set_page_config method. Additionally, it adds a title to the page combining the
    icon and the title fetched from the configuration.
    """
    # load page config
    page_config = next(
        item
        for item in toml.load(PAGES_CONFIG_PATH).get("pages")
        if file_path.as_posix().endswith(item.get("path"))
    )

    # configure page
    page_title = page_config.get("name")
    page_icon = page_config.get("icon")

    st.set_page_config(
        page_title=f"FCE | {page_title}",
        page_icon="🏒",
        # layout="wide",
        layout="centered",
    )

    # add page title
    st.write(f"# {page_icon} {page_title}")


def style_standings_df(df: pd.DataFrame) -> None:
    """Style standings data frame.

    Parameters:
    -----------
    df : pd.DataFrame
        Data frame with standings.

    Returns:
    --------
    None
    """
    # add rank into index
    df = df.reset_index(drop=True)
    df["rank"] = df.index + 1
    df = df.set_index(["rank"])

    # style data
    st.dataframe(
        data=df,
        column_order=STANDDINGS_DF_COLUMN_CONFIG.keys(),
        column_config=STANDDINGS_DF_COLUMN_CONFIG,
        # display dataframe in full (35 pixel is row height, 3 pixels is borders height)
        height=(len(df) + 1) * 35 + 3,
    )
