from pathlib import Path

import streamlit as st
from st_pages import show_pages_from_config
from utils.style import style_page

style_page(file_path=Path(__file__))
show_pages_from_config()

st.write(
    """
    ##### Welcome to Frozen Facts Center, your ultimate destination for all things data \
    and analytics in the thrilling world of ice hockey!
    
    Step onto the ice with us as we delve deep into the numbers, uncovering insights, trends, 
    and stories that go beyond the game's surface. Whether you're a die-hard fan, a seasoned 
    analyst, or someone just starting to explore the fascinating intersection of data and sports, 
    this platform is your gateway to unlocking the hidden narratives within the rink.
    
    From player performance metrics to team strategies, game-changing trends to historical data 
    retrospectives, we're here to break down the game using the power of analytics. Our goal is 
    to fuel your passion for hockey by providing comprehensive analyses and compelling 
    visualizations that bring the numbers to life.
    
    Join us in exploring the dynamic world of hockey through a data-driven lens. Get ready 
    to witness the game in a whole new light with Frozen Facts Center - where numbers meet the ice!
    """
)
