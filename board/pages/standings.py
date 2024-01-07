from pathlib import Path

import streamlit as st
from st_files_connection import FilesConnection

from utils.style import style_page, style_standings_df

style_page(file_path=Path(__file__))

# read data
conn = st.connection("s3", type=FilesConnection)
df = conn.read(
    path="frozen-facts-center-prod/fact_standings.parquet",
    input_format="parquet",
    ttl=600,
)

# add team records in games
for record_type in ("home", "away", "last_10", "so"):
    record_cols = [
        f"{dim}_{record_type}" for dim in ["wins", "losses", "ots"] if f"{dim}_{record_type}" in df
    ]
    df[f"record_{record_type}"] = df[record_cols].astype(int).astype(str).apply("-".join, axis=1)

# add season filter
filter_season = st.selectbox(
    label="Season",
    options=[f"{season}-{season + 1}" for season in df.season.astype(int).unique()],
    label_visibility="hidden",
)
df = df.loc[df.season == int(filter_season[:4])]

# create tabs
tab_division, tab_conference, tab_league = st.tabs(["Division", "Conference", "League"])

with tab_division:
    for conference in sorted(df.conference.unique()):
        st.write(f"## {conference}")

        for division in sorted(df.loc[df.conference == conference].division.unique()):
            st.write(f"### {division}")
            style_standings_df(df=df.loc[df.division == division])

with tab_conference:
    for conference in sorted(df.conference.unique()):
        st.write(f"## {conference}")
        style_standings_df(df=df.loc[df.conference == conference])

with tab_league:
    st.write("## League")
    style_standings_df(df=df)
