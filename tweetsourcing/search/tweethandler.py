import os
import tweepy, requests

def create_api():
    """Creates api object from tweepy using api auth credentials.
    """
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_SECRET_KEY'))
    auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))
    return tweepy.API(auth)

    