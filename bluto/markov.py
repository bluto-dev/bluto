"""Rough sample app of Markov Generator"""

import os
import re

import markovify
from atproto import Client, IdResolver


def get_all_posts(username):
    """Returns list of text entries for <username>'s last 100 posts'"""
    client = Client()

    user_identifier = IdResolver().handle.resolve(username)

    posts = list(client.app.bsky.feed.post.list(user_identifier, limit=100).records.values())

    return [post.text for post in posts]


def get_avatar_url(username):
    """Get the URL of <username>'s avatar"""
    client = Client()

    # Technically the get_profile endpoint shouldn't require authentication
    # but right now this works
    # if we do end up needing to authenticate for this we should
    # login using an exported session string instead of creating a new session every time
    client.login(os.getenv("BLUESKY_USERNAME"), os.getenv("BLUESKY_PASSWORD"))

    user_identifier = IdResolver().handle.resolve(username)
    profile = client.app.bsky.actor.get_profile({"actor": user_identifier})

    return profile.avatar


def remove_twitlonger(tweet_list):
    """Removes all tweets that have a twitlonger link in them"""
    return [re.sub(r" \S*…[^']*", "", tweet) for tweet in tweet_list]


def make_posts(username, num_posts):
    """Produce an array of generated posts"""
    data = remove_twitlonger(get_all_posts(username))
    model = markovify.Text(" ".join(data))

    return {
        "username": username,
        "profile_url": get_avatar_url(username),
        "tweets": [model.make_short_sentence(140) for i in range(num_posts)],
        "long": [model.make_short_sentence(240) for i in range(2)]}
