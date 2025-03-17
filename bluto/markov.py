"""Rough sample app of Markov Generator"""

import os
import re

import markovify
import twitter

TWEET_LIMIT = 200


def generate(text_model, size, bound):
    """Makes 140 character tweets"""
    return [text_model.make_short_sentence(size) for i in range(bound)]


def get_all_tweets(username):
    """Spawns api and gets last 2000 tweets"""
    api = new_api()
    tweets = get_tweets(api, username)

    for _ in range(20):
        tweets += get_tweets(api, username, since=tweets[len(tweets) - 1].id)

    return tweets


def get_profile_url(api, username):
    """Get a big version of the profile image"""
    user = (api.GetUser(screen_name=username),)

    return user[0].profile_image_url.replace("normal", "400x400")


def remove_twitlonger(tweet_list):
    """Removes all tweets that have a twitlonger link in them"""
    return [re.sub(r" \S*…[^']*", "", tweet) for tweet in tweet_list]


def make_tweets(username, num_tweets):
    """Produce an array of generated tweets"""
    api = new_api()
    data = remove_twitlonger([tweet.text for tweet in get_all_tweets(username)])
    model = make_markov_model(data)

    return {
        "username": username,
        "profile_url": get_profile_url(api, username),
        "tweets": generate(model, 140, num_tweets),
        "long": generate(model, 240, 2),
    }


# Utility
def new_api():
    """Wrapper around spawning twitter api"""
    return twitter.Api(
        consumer_key=os.environ["TWITTER_API_KEY"],
        consumer_secret=os.environ["TWITTER_API_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
    )


def get_tweets(api, username, since=None):
    """Wrapper around api request"""
    return api.GetUserTimeline(
        screen_name=username,
        count=TWEET_LIMIT,
        include_rts=False,
        trim_user=False,
        exclude_replies=True,
        max_id=since,
    )


def make_markov_model(tweets):
    """Wrapper around making Markov Chain"""
    return markovify.Text(" ".join(tweets))
