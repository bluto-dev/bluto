# Tests for markov_app.py
import os

import markov_app as mkv


def test_generate():
    """Make sure we generate the right number of tweets"""
    tweets = ["the", "big", "cat", "jumped"]

    for i in range(10):
        result = mkv.generate(tweets, i)
        assert len(result) == i


def test_environ():
    """Test for environment varibles"""
    env_vars = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_SECRET",
    ]

    for key in env_vars:
        assert key in os.environ
