import os
import tweepy, requests


def create_api() -> tweepy.API:
    """Creates api object from tweepy using api auth credentials."""
    auth = tweepy.OAuthHandler(
        os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_SECRET_KEY")
    )
    auth.set_access_token(
        os.environ.get("TWITTER_ACCESS_TOKEN"),
        os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
    )
    return tweepy.API(auth)


def retrieve_tweet(api_object: tweepy.API, tweet_url: str):
    """Used to get a tweet object from authorized api object.

    :param api_object: Tweepy api object
    :type api_object: tweepy.API
    :param tweet_url: URL of desired tweet to analyze
    :type tweet_url: str
    :return: Tweet object
    """
    tweet_id = tweet_url.split("/status/")[1]
    return api_object.get_status(tweet_id, tweet_mode="extended")
