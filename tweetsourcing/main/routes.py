from flask import Blueprint, render_template, request, url_for, flash
from tweetsourcing.search import tweethandler, parse
from tweetsourcing.main.forms import TweetForm
from tweetsourcing import twitter_api

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("", methods=("GET", "POST"))
def home():
    form = TweetForm()
    if request.method == "POST":
        tweet_url = form.tweet_url.data
        tweet_embed, tweet_status = tweethandler.retrieve_embedded_tweet(
            twitter_api, tweet_url=tweet_url, include_obj=True
        )
        tweet_images = tweethandler.pull_images(api_object=twitter_api, tweet_url=tweet_url)
        query = parse.query_from_parse(tweet_status.full_text)
        return render_template(
            "home.html",
            title="TweetSourcing",
            tweet_embed=tweet_embed,
            tweet_images=tweet_images,
            form=form,
            query=query
        )

    else:
        return render_template(
            "home.html",
            title="TweetSourcing",
            tweet_status=None,
            tweet_images=None,
            query=None,
            form=form
        )
