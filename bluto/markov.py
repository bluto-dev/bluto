"""Rough sample app of Markov Generator"""

import os
import re
from pathlib import Path

import markovify
from atproto import Client
from atproto import IdResolver
from atproto import SessionEvent


def get_all_posts(username):
    """Returns list of text entries for <username>'s last 100 posts'"""
    # We don't need to authenticate this request
    client = Client()

    user_id = IdResolver().handle.resolve(username)

    posts = list(client.app.bsky.feed.post.list(user_id, limit=100).records.values())

    return [post.text for post in posts]


def get_avatar_url(username):
    """Get the URL of <username>'s avatar"""
    client = get_client()

    user_id = IdResolver().handle.resolve(username)

    profile = client.app.bsky.actor.get_profile({"actor": user_id})

    return profile.avatar


def remove_twitlonger(tweet_list):
    """Removes all tweets that have a twitlonger link in them"""
    return [re.sub(r" \S*…[^']*", "", tweet) for tweet in tweet_list]


def make_posts(username, num_posts):
    """Produce an array of generated posts"""
    data = remove_twitlonger(get_all_posts(username))
    model = make_markov_model(data)

    return {
        "username": username,
        "profile_url": get_avatar_url(username),
        "tweets": [model.make_short_sentence(140) for i in range(num_posts)],
        "long": [model.make_short_sentence(240) for i in range(2)],
    }


# Useful for Behave testing
def make_markov_model(data):
    """Wrapper around Markovify call"""
    return markovify.Text(" ".join(data))


# Client handling
def get_session():
    try:
        with Path.open("session.txt") as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_session(session_string):
    with Path.open("session.txt", "w") as f:
        f.write(session_string)


def on_session_change(event, session):
    if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
        save_session(session.export())


def get_client():
    client = Client()
    client.on_session_change(on_session_change)

    session_string = get_session()
    if session_string:
        client.login(session_string=session_string)
    else:
        client.login(os.getenv("BLUESKY_USERNAME"), os.getenv("BLUESKY_PASSWORD"))

    return client
