"""Rough sample app of Markov Generator"""

import os
import re
from pathlib import Path

import markovify
from atproto import Client
from atproto import IdResolver
from atproto import SessionEvent
from flask import abort


def get_all_posts(did):
    """Returns list of text entries for last 100 posts for this DID"""
    # We don't need to authenticate this request
    client = Client()

    posts = list(client.app.bsky.feed.post.list(did, limit=100).records.values())

    return [post.text for post in posts]


def get_avatar_url(did):
    """Get the URL of avatar for this DID"""
    client = get_client()

    profile = client.app.bsky.actor.get_profile({"actor": did})

    return profile.avatar


def make_posts(username, num_posts):
    """Produce an array of generated posts"""
    did = get_did_else_abort(username)

    user_posts = get_all_posts(did)

    return {
        "username": username,
        "profile_url": get_avatar_url(did),
        "posts": make_markov_sentences(user_posts, 140, num_posts),
        "long": make_markov_sentences(user_posts, 240, 2),
    }


def make_markov_sentences(user_posts, max_length, num_to_make):
    """Clean up user post data, feed into Markov model, get a list of new posts"""

    # Old twitlonger removal regex, update??
    cleaned_posts = [re.sub(r" \S*…[^']*", "", post) for post in user_posts]

    model = markovify.Text(" ".join(cleaned_posts))

    return [
        model.make_short_sentence(
            max_chars=max_length,
            test_output=False,
        )
        for i in range(num_to_make)
    ]


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


def get_did_else_abort(username):
    did = IdResolver().handle.resolve(username)
    if did is None:
        abort(404)
    return did
