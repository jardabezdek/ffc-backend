"""Lambda function handler example for future generations."""

import json

import requests

from utils import get_hello_mesage


def handler(event: dict, context):
    """Handle the main functionality."""
    print(f"event: {json.dumps(event)}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain",
        },
        "body": {
            # local dependency test
            "hello_message": get_hello_mesage(),
            # lambda dependency test
            "event_path": event.get("path"),
            # third-party dependency test
            "are_requests_working": requests.get("https://api.github.com/emojis").ok,
        },
    }
