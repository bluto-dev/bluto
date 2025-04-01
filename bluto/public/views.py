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


@blueprint.route("/posts", methods=["GET"])
def get_posts():
    """Makes posts for requested user and return rendered template"""
    bluesky_handle = request.args["bluesky_handle"]
    posts = mkv.make_posts(bluesky_handle, 30)

    return render_template(
        "public/results.html",
        username=bluesky_handle,
        posts=posts["posts"],
        long_posts=posts["long"],
        profile_url=posts["profile_url"],
        num_posts=posts["num_posts"],
    )


@blueprint.route("/api/<bluesky_handle>", methods=["GET"])
def get_api_posts(bluesky_handle):
    """Makes posts for requested user and return as json"""
    posts = mkv.make_posts(bluesky_handle, 30)
    return jsonify(posts)


@blueprint.route("/api/ping", methods=["GET"])
def ping():
    """Simple health check"""
    return "pong", 200
