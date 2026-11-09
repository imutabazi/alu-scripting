#!/usr/bin/python3
"""Recursive function to count keywords in hot article titles of a subreddit."""
import requests


def count_words(subreddit, word_list, after=None, counts={}):
    """Recursively fetch hot titles and print sorted keyword counts."""
    if subreddit is None or not isinstance(subreddit, str):
        return

    if after is None:
        counts.clear()
        for w in word_list:
            w_lower = w.lower()
            counts[w_lower] = counts.get(w_lower, 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "custom-script:v1.0 (by /u/alu-student)"}
    params = {"after": after} if after else {}

    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False
    )

    if response.status_code != 200:
        return

    try:
        data = response.json().get("data", {})
        children = data.get("children", [])

        word_weights = {}
        for w in word_list:
            w_lower = w.lower()
            word_weights[w_lower] = word_weights.get(w_lower, 0) + 1

        for child in children:
            title_words = child.get("data", {}).get("title", "").lower().split()
            for word in title_words:
                if word in counts:
                    counts[word] += word_weights[word]

        next_after = data.get("after")
        if next_after is not None:
            return count_words(subreddit, word_list, next_after, counts)
        else:
            sorted_counts = sorted(
                [item for item in counts.items() if item[1] > 0],
                key=lambda x: (-x[1], x[0])
            )
            for word, count in sorted_counts:
                print("{}: {}".format(word, count))
    except Exception:
        return
