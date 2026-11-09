#!/usr/bin/python3
"""Module to query Reddit API for subscriber count of a subreddit."""
import requests


def number_of_subscribers(subreddit):
    """Return subscriber count for a subreddit, or 0 if invalid."""
    if subreddit is None or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "custom-script:v1.0 (by /u/alu-student)"}

    response = requests.get(
        url, headers=headers, allow_redirects=False
    )
    if response.status_code == 200:
        results = response.json().get("data", {})
        return results.get("subscribers", 0)
    return 0
