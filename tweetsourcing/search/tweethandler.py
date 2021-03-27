"""tweethandler contains the TweetHandler class that wraps around tweepy's
API object. Functions as the main way to interact with tweets and twitter's
api.
"""
import os
from flask.globals import current_app
import tweepy


class TweetHandler(tweepy.API):
    """Wrapper for the tweepy.API object to tie together and add some functionality.

    :param api_key: Twitter api key
    :param secret_key: Twitter secret key
    :param access_token: Twitter access token
    :param access_token_secret: Twitter access token secret
    """

    def __init__(
        self, api_key, secret_key, access_token=None, access_token_secret=None
    ):
        super().__init__(self)
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.tweet = None

        oauth_handler = tweepy.OAuthHandler(self.api_key, self.secret_key)
        if self.access_token and self.access_token_secret:
            oauth_handler.set_access_token(self.access_token, self.access_token_secret)
        self.auth = oauth_handler

    def __str__(self) -> str:
        if self.tweet:
            return f"Tweet: {self.tweet.full_text}"
        else:
            return f"Tweet: {self.tweet}"

    def __bool__(self) -> bool:
        if self.tweet:
            return True
        else:
            return False

    def retrieve_tweet(self, tweet_url: str) -> tweepy.Status:
        """Used to get a Status object from a url string.

        :param tweet_url: URL of desired tweet to analyze
        :type tweet_url: str
        :return: tweepy.Status
        """
        tweet_id = tweet_url.split("/status/")[1]
        self.tweet = self.get_status(tweet_id, tweet_mode="extended")
        return self.tweet

    def retrieve_embedded_tweet(self, tweet_url: str, include_obj: bool = False):
        """Used to get the html for an embedded tweet.

        :param api_object: Tweepy api object that is used for the retrieval method
        :type api_object: tweepy.API
        :param tweet_url: URL of desired tweet to embed
        :type tweet_url: str
        :param include_obj: True to include tweepy.Status obj in return value
        :type include_obj: boolean
        :return: oembed HTML or (oembed HTML, tweepy.Status)
        :rtype: str, tweepy.Status
        """
        try:
            tweet = self.get_oembed(
                url=tweet_url, hide_thread="true", align="center", dnt="true"
            )
        except Exception as e:
            current_app.logger.error(
                f"Oembed tweet error, message: {e}; URL attempted to retrieve: {tweet_url}"
            )
        if include_obj:
            return (tweet["html"], self.retrieve_tweet(tweet_url))
        return tweet["html"]

    def pull_images(self, status_object=None, **kwargs):
        """Used to pull image urls from the tweet if any exists

        :param status_object: Status object pulled from a tweet url with retrieve_tweet
        :type status_object: tweepy.Status
        :return: Iterable container of unique image urls.
        :rtype: Set
        """
        if status_object is None and ("api_object" in kwargs and "tweet_url" in kwargs):
            status_object = self.retrieve_tweet(
            kwargs["tweet_url"]
            )
        try:
            tweet_images = status_object.entities["media"]
            image_urls = []
        except KeyError:
            return None
        except AttributeError:
            return None
        for image in tweet_images:
            image_urls.append(image["media_url"])
        return image_urls