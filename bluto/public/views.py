"""Public section, including homepage and signup."""
from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

import bluto.markov as mkv

blueprint = Blueprint("public", __name__, static_folder="../../static")

@blueprint.route("/")
def index():
    """Main page"""
    return render_template("public/landing.html")

@blueprint.route("/tweets", methods=["GET"])
def get_tweets():
    """Makes tweets for requested user and return rendered template"""
    twitter_handle = request.args["twitter_handle"]
    tweets = mkv.make_tweets(twitter_handle, 30)

    return render_template(
        "public/results.html",
        username=twitter_handle,
        tweets=tweets["tweets"],
        long_tweets=tweets["long"],
        profile_url=tweets["profile_url"])

@blueprint.route("/api/<twitter_handle>", methods=["GET"])
def get_api_tweets(twitter_handle):
    """Makes tweets for requested user and return as json"""
    tweets = mkv.make_tweets(twitter_handle, 30)
    return jsonify(tweets)

@blueprint.route("/api/ping", methods=["GET"])
def ping():
    """Simple health check"""
    return "pong", 200
