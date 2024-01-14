"""
Frozen Facts Center - Standings page

This script provides a Streamlit web application for viewing NHL standings, including regular 
season and playoff data. It reads data from S3 storage, allows users to filter by season, and 
displays standings organized by division, conference, league, and playoff tabs.
"""

from pathlib import Path

import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection
from utils.style import style_page, style_standings_df

DATA_PATH_STANDINGS_REGULAR = "frozen-facts-center-prod/fact_standings_regular.parquet"
DATA_PATH_STANDINGS_PLAYOFF = "frozen-facts-center-prod/fact_standings_playoff.parquet"
TAB_NAMES = [
    "Division",
    "Conference",
    "League",
    "Play-off",
]


def main() -> None:
    """Main function to configure and display Standings page.

    This function sets the page style, reads data, filters data based on the selected season,
    and creates tabs for displaying standings by division, conference, league, and playoff.
    Each tab contains relevant information, and the page layout is organized using Streamlit's
    tabs feature.

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """
    style_page(file_path=Path(__file__))

    # read data
    df_regular, df_playoff = read_data()

    # filter season
    filter_season = st.selectbox(
        label="Season", options=df_regular.season_long.unique(), label_visibility="hidden"
    )
    df_regular = df_regular.loc[df_regular.season_long == filter_season]
    df_playoff = df_playoff.loc[df_playoff.season_long == filter_season]

    # create tabs
    tab_division, tab_conference, tab_league, tab_playoff = st.tabs(tabs=TAB_NAMES)

    with tab_division:
        for conference in sorted(df_regular.conference.unique()):
            st.write(f"## {conference}")

            for division in sorted(
                df_regular.loc[df_regular.conference == conference].division.unique()
            ):
                st.write(f"### {division}")
                style_standings_df(df=df_regular.loc[df_regular.division == division])

    with tab_conference:
        for conference in sorted(df_regular.conference.unique()):
            st.write(f"## {conference}")
            style_standings_df(df=df_regular.loc[df_regular.conference == conference])

    with tab_league:
        st.write("## League")
        style_standings_df(df=df_regular)

    with tab_playoff:
        create_playoff_tab_content(df=df_playoff)


def read_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read standings data from S3 storage.

    This function reads regular season standings and playoff standings
    from specified paths in parquet format. The TTL (Time To Live) is set to 600
    seconds for both dataframes to cache the data for improved performance.

    Parameters:
    -----------
    None

    Returns:
    --------
    tuple[pd.DataFrame, pd.DataFrame]
        A tuple containing two dataframes - one for regular season standings and the other
        for playoff standings.
    """
    conn = st.connection("s3", type=FilesConnection)

    return (
        conn.read(path=DATA_PATH_STANDINGS_REGULAR, input_format="parquet", ttl=600),
        conn.read(path=DATA_PATH_STANDINGS_PLAYOFF, input_format="parquet", ttl=600),
    )


def create_playoff_tab_content(df: pd.DataFrame) -> None:
    """Create content for the playoff tab.

    This function takes a DataFrame containing playoff standings and creates subheaders for each
    playoff round along with details of matchups, including scores, teams, and match results.
    It formats and displays the information using Streamlit components.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing playoff standings.

    Returns:
    --------
    None
    """
    for round_ in sorted(df.playoff_round.unique(), reverse=True):
        st.subheader(body="Final" if round_ == 4 else f"Round {round_}", divider="grey")

        for matchup in df.loc[df.playoff_round == round_].matchup.unique():
            df_matchup = df.loc[(df.playoff_round == round_) & (df.matchup == matchup)]

            render_matchup_headline(df=df_matchup)
            render_matchup_matches(df=df_matchup)

            # add empty space
            st.write("#####")


def render_matchup_headline(df: pd.DataFrame) -> None:
    """Render a matchup headline in a Streamlit app based on the final match scores.

    This function takes a DataFrame containing playoff series information, extracts
    the final match scores, and renders a stylized matchup headline in a Streamlit app.
    The headline includes team logos, names, and the final score.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing playoff series information.

    Returns:
    --------
    None
        This function renders the matchup headline in a Streamlit app.
    """
    (
        matchup_win_team,
        matchup_loss_team,
        matchup_win_team_score,
        matchup_loss_team_score,
        matchup_win_team_logo_url,
        matchup_loss_team_logo_url,
    ) = extract_final_match_score(df=df)

    # center all the columns content
    st.markdown(
        body="""
        <style>
            div[data-testid="column"]:nth-of-type(2) {text-align: center;} 
            div[data-testid="column"]:nth-of-type(3) {text-align: center;} 
            div[data-testid="column"]:nth-of-type(4) {text-align: center;} 
        </style>
        """,
        unsafe_allow_html=True,
    )

    # create columns
    column_layout = [2, 3, 1, 3, 2]
    _, col2, col3, col4, _ = st.columns(spec=column_layout)

    def render_logo_and_name(name: str, logo_url: str) -> None:
        st.markdown(
            body=f"<img src='{logo_url}' alt='drawing' width='80'/>",
            unsafe_allow_html=True,
        )
        st.markdown(body=f"**{name}**")

    with col2:
        render_logo_and_name(name=matchup_win_team, logo_url=matchup_win_team_logo_url)

    with col3:
        st.markdown(body=f"### {matchup_win_team_score}-{matchup_loss_team_score}")

    with col4:
        render_logo_and_name(name=matchup_loss_team, logo_url=matchup_loss_team_logo_url)


def extract_final_match_score(df: pd.DataFrame) -> tuple[str, str, int, int, str, str]:
    """Extract final match scores from the DataFrame representing a playoff series.

    This function takes a DataFrame containing playoff series information and extracts the final
    match scores, winning and losing team names. It returns a tuple containing the winning team
    name, losing team name, winning team score, and losing team score.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing playoff series information.

    Returns:
    --------
    tuple[str, str, int, int, str, str]
        A tuple containing the winning team name, losing team name, winning team score,
        losing team score, winning team logo, and losing team logo.
    """
    cols = [
        "home_team_full_name",
        "away_team_full_name",
        "home_team_match_score",
        "away_team_match_score",
        "home_team_logo_url",
        "away_team_logo_url",
    ]

    # extract values from the last match of the series
    home_team, away_team, home_team_score, away_team_score, home_logo, away_logo = (
        df.tail(1).loc[:, cols].values[0]
    )

    return (
        home_team if home_team_score == 4 else away_team,
        away_team if home_team_score == 4 else home_team,
        home_team_score if home_team_score == 4 else away_team_score,
        away_team_score if home_team_score == 4 else home_team_score,
        home_logo if home_team_score == 4 else away_logo,
        away_logo if home_team_score == 4 else home_logo,
    )


def render_matchup_matches(df: pd.DataFrame) -> None:
    """Render playoff matchup matches.

    This function takes a DataFrame containing playoff series information and renders the individual
    matches in a stylized format. The rendered information includes match details such as date,
    teams, scores, and additional indicators like overtime (OT) and final series scores.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing playoff series information.

    Returns:
    --------
    None
        This function renders the matchup matches in a Streamlit app.
    """
    column_layout = [1, 2, 1]
    match_info_column = 1

    with st.columns(spec=column_layout)[match_info_column]:
        formatted_matches = [
            "({})   {}   {} {}-{} {} {}   ({}-{})".format(
                row.match,
                row.day_month,
                row.home_team_abbrev_name,
                row.home_team_score,
                row.away_team_score,
                row.away_team_abbrev_name,
                "(OT)" if row.period_type == "OT" else " " * 4,
                row.home_team_match_score,
                row.away_team_match_score,
            )
            for _, row in df.iterrows()
        ]

        st.text("\n".join(formatted_matches))


if __name__ == "__main__":
    main()
