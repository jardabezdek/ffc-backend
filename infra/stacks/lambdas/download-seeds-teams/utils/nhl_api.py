"""Util functions for lambda function."""

import json

import requests

URL_STANDINGS = "https://api-web.nhle.com/v1/standings"


def get_current_standings() -> dict:
    """Retrieve the current standings.

    Returns:
    --------
    dict or None
        A dictionary containing the current standings information if the request is successful.
        Returns None if there are issues in retrieving the standings data.
    """
    response = requests.get(url=f"{URL_STANDINGS}/now")

    if response.ok:
        standings = json.loads(response.text).get("standings")
        print("✅ Standings loaded successfully!")

    else:
        print("❌ Error: Standings were NOT loaded!")

    return standings
