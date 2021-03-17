from flask import Blueprint, render_template, request, url_for

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("", methods=("GET", "POST"))
def home():
    if request.method == "POST":
        tweet_url = request.form["tweet_url"]
    return render_template("home.html", title="TweetSourcing")
