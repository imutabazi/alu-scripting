#!/usr/bin/python3
"""Recursive function to query Reddit API for all hot article titles."""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Return a list containing titles of all hot articles for a subreddit."""
    if subreddit is None or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "custom-script:v1.0 (by /u/alu-student)"}
    params = {"after": after} if after else {}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False
    )

    if response.status_code != 200:
        return None

    try:
        data = response.json().get("data", {})
        children = data.get("children", [])
        for child in children:
            hot_list.append(child.get("data", {}).get("title"))

        next_after = data.get("after")
        if next_after is not None:
            return recurse(subreddit, hot_list, next_after)
        return hot_list
    except Exception:
        return None
