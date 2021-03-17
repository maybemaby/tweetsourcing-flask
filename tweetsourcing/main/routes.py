from flask import Blueprint, render_template, request, url_for, flash
from tweetsourcing.search import tweethandler
from tweetsourcing.main.forms import TweetForm

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("", methods=("GET", "POST"))
def home():
    form = TweetForm()
    if request.method == "POST":
        tweet_url = form.tweet_url.data
        tweet_status = tweethandler.retrieve_tweet(
            tweethandler.create_api(), tweet_url=tweet_url
        )
        tweet_images = tweethandler.pull_images(tweet_status)
        return render_template(
            "home.html",
            title="TweetSourcing",
            tweet_status=tweet_status.full_text,
            tweet_images=tweet_images,
            form=form,
        )

    else:
        return render_template(
            "home.html",
            title="TweetSourcing",
            tweet_status=None,
            tweet_images=None,
            form=form,
        )
