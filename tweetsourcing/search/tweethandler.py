import os
import tweepy, requests

# Currently using twitter_api variable under tweetsourcing instead of this.
# Not sure which method is better.
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

def retrieve_tweet(api_object: tweepy.API, tweet_url: str) -> tweepy.Status:
    """Used to get a tweet object from authorized api object.

    :param api_object: Tweepy api object
    :type api_object: tweepy.API
    :param tweet_url: URL of desired tweet to analyze
    :type tweet_url: str
    :return: tweepy.Status
    """
    tweet_id = tweet_url.split("/status/")[1]
    return api_object.get_status(tweet_id, tweet_mode="extended")

def retrieve_embedded_tweet(api_object: tweepy.API, tweet_url: str):
    """Used to get the html for an embedded tweet.

    :param api_object: Tweepy api object that is used for the retrieval method
    :type api_object: tweepy.API
    :param tweet_url: URL of desired tweet to embed
    :type tweet_url: str
    :return: oembed HTML
    :rtype: HTML
    """
    try:
        tweet = api_object.get_oembed(url=tweet_url, hide_thread=True, align='center')
    except Exception as e:
        print(f'Error occured, message: {e}; URL attempted to retrieve: {tweet_url}')
    return tweet.html

def pull_images(status_object):
    """Used to pull image urls from the tweet if any exists

    :param status_object: Status object pulled from a tweet url with retrieve_tweet
    :type status_object: tweepy.Status
    :return: Iterable container of unique image urls.
    :rtype: Set
    """
    try:
        tweet_images = status_object.entities["media"]
        image_url = set()
    except KeyError:
        return None
    for image in tweet_images:
        image_url.add(image["media_url"])
    return image_url