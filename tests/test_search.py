from tests.conftest import twitter_api
from tweetsourcing.search.tweethandler import create_api, retrieve_tweet, retrieve_embedded_tweet
import pytest
import tweetsourcing.search
import tweepy


class TestTweetHandler:
    """Testing tweethandler functions"""

    def test_api_creation(self):
        # Creates and asserts successful api object creation.
        api_object = create_api()
        assert type(api_object) is tweepy.API

    def test_retrieve_tweet(self, twitter_api):
        # tests retrieve_tweet function
        tweet = retrieve_tweet(
            twitter_api, "https://twitter.com/thepsf/status/1266007827061116929?lang=en"
        )
        assert type(tweet) is tweepy.Status
        assert tweet.full_text == '''Python users are very keen on multitasking. The mean number of purposes chosen in the question “What do you use Python for?” was 3.9. \n\nhttps://t.co/f9kEsnN2nA #pythondevsurvey https://t.co/I1wh7pmGoK'''

    def test_retrieve_embedded_tweet(self, twitter_api):
        # test retrieve_embedded_tweet function
        tweet = retrieve_embedded_tweet(twitter_api, 'https://twitter.com/thepsf/status/1266007827061116929?lang=en')
        assert bool(tweet)
        assert 'data-dnt="true"' in tweet
        assert 'Python users are very keen on multitasking. The mean number of purposes chosen in the question “What do you use Python for?” was 3.9. \n\nhttps://t.co/f9kEsnN2nA #pythondevsurvey https://t.co/I1wh7pmGoK'
        assert '<blockquote' in tweet and '</blockquote>' in tweet
