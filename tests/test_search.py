import tweetsourcing.search.parse as parse
from tests.conftest import tweet_status, twitter_api
from tweetsourcing.search.tweethandler import (
    create_api,
    pull_images,
    retrieve_tweet,
    retrieve_embedded_tweet,
)
import pytest
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
        assert (
            tweet.full_text
            == """Python users are very keen on multitasking. The mean number of purposes chosen in the question “What do you use Python for?” was 3.9. \n\nhttps://t.co/f9kEsnN2nA #pythondevsurvey https://t.co/I1wh7pmGoK"""
        )

    def test_retrieve_embedded_tweet(self, twitter_api):
        # test retrieve_embedded_tweet function
        tweet = retrieve_embedded_tweet(
            twitter_api, "https://twitter.com/thepsf/status/1266007827061116929?lang=en"
        )
        assert bool(tweet)
        assert 'data-dnt="true"' in tweet
        assert "Python users are very keen on multitasking. The mean number of purposes chosen in the question “What do you use Python for?” was 3.9. \n\nhttps://t.co/f9kEsnN2nA #pythondevsurvey https://t.co/I1wh7pmGoK"
        assert "<blockquote" in tweet and "</blockquote>" in tweet

    def test_pull_images_no_status(self, twitter_api):
        # test pull_images function wihout an included Status object
        images = pull_images(
            api_object=twitter_api,
            tweet_url="https://twitter.com/thepsf/status/1266007827061116929?lang=en",
        )
        assert bool(images)
        assert len(images) == 1
        assert images.pop() == "http://pbs.twimg.com/media/EZHDaK4XsAE774T.jpg"

    def test_pull_images_no_pic(self, twitter_api):
        # testing pull_images with a tweet with no image.
        images = pull_images(tweet_status)
        assert images is None


class TestParse:
    """Test the parse module of tweetsourcing.search"""

    def test_extract_kwords(self):
        # Test successful keyword extractions
        keywords = parse.extract_kwords(
            "Which words from this tweet will be the extracted words?"
        )
        assert "extracted words" in keywords
        assert "words" in keywords
        assert "tweet" in keywords
        assert "from" not in keywords and "will" not in keywords

    def test_create_query(self):
        # Test query creating from list of keywords and filtering out words shorter than 3 letters
        keyword_list = ["extracted words", "words", "tweet", "be", "to"]
        query = parse.create_query(keyword_list)
        with pytest.raises(ValueError):
            query.index("be")
        with pytest.raises(ValueError):
            query.index("to")
        assert query == "extracted words OR words OR tweet"

    def test_query_from_parse(self):
        # Test the helper function from parse
        query = parse.query_from_parse(
            "Which words from this tweet will be the extracted words?"
        )
        assert query == "extracted words OR words OR tweet"
