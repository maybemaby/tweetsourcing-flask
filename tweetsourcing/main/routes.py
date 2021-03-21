from flask import Blueprint, render_template, request, url_for, flash, session
from tweetsourcing.search import tweethandler, parse, gsearch
from tweetsourcing.main.forms import TweetForm, SearchForm
from tweetsourcing import twitter_api

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("", methods=("GET", "POST"))
def home():
    form = TweetForm()
    confirm_form = SearchForm()
    if request.method == "POST" and form.submit():
        tweet_url = form.tweet_url.data
        tweet_embed, tweet_status = twitter_api.retrieve_embedded_tweet(
            tweet_url=tweet_url, include_obj=True
        )
        tweet_images = twitter_api.pull_images(status_object=tweet_status)
        query, or_terms = parse.query_from_parse(tweet_status.full_text)
        session["query"] = query
        return render_template(
            "home.html",
            title="TweetSourcing",
            tweet_embed=tweet_embed,
            tweet_images=tweet_images,
            form=form,
            query=query,
            or_terms=or_terms,
            confirm_form=confirm_form
        )
    else:
        return render_template(
            "home.html",
            title="TweetSourcing",
            tweet_status=None,
            tweet_images=None,
            query=None,
            form=form,
        )


@bp.route("search", methods=["POST"])
def search():
    form = SearchForm()
    query = form.query.data
    or_terms = form.or_terms.data
    kwords = or_terms.split("|")
    kwords += query
    matches = gsearch.search_helper(query, tweet_kwords=kwords, orTerms=or_terms)
    return render_template(
        "results.html", title="TweetSourcing - Results", matches=matches.values()
    )
