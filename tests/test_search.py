import os
import tweetsourcing.search.gsearch as gsearch
import pytest
import tweepy
from tests.conftest import tweet_status, twitter_api
import tweetsourcing.search.parse as parse
from tweetsourcing.search.tweethandler import TweetHandler

# TODO: Create test for no items in result objects
# TODO: Test for handling newspaper.article read taking too long


class TestTweetHandler:
    """Testing tweethandler functions"""

    def test_api_creation(self):
        # Creates and asserts successful api object creation.
        api_object = TweetHandler(
            api_key=os.environ.get("TWITTER_API_KEY"),
            secret_key=os.environ.get("TWITTER_SECRET_KEY"),
            access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
        )
        assert type(api_object.me()) is tweepy.User

    def test_api_fail(self):
        # Tests for failure of api creation due to incorrect keys
        api_object = TweetHandler(api_key="notthekey", secret_key="alsonotthekey")
        with pytest.raises(tweepy.TweepError):
            api_object.me() == None

    def test_retrieve_tweet(self, twitter_api):
        # tests retrieve_tweet function
        tweet = twitter_api.retrieve_tweet(
            "https://twitter.com/thepsf/status/1266007827061116929?lang=en"
        )
        assert type(tweet) is tweepy.Status
        assert (
            tweet.full_text
            == """Python users are very keen on multitasking. The mean number of purposes chosen in the question “What do you use Python for?” was 3.9. \n\nhttps://t.co/f9kEsnN2nA #pythondevsurvey https://t.co/I1wh7pmGoK"""
        )

    def test_retrieve_embedded_tweet(self, twitter_api):
        # test retrieve_embedded_tweet function
        tweet = twitter_api.retrieve_embedded_tweet(
            "https://twitter.com/thepsf/status/1266007827061116929?lang=en"
        )
        assert bool(tweet)
        assert 'data-dnt="true"' in tweet
        assert "Python users are very keen on multitasking. The mean number of purposes chosen in the question “What do you use Python for?” was 3.9. \n\nhttps://t.co/f9kEsnN2nA #pythondevsurvey https://t.co/I1wh7pmGoK"
        assert "<blockquote" in tweet and "</blockquote>" in tweet

    def test_pull_images_no_status(self, twitter_api):
        # test pull_images function wihout an included Status object
        images = twitter_api.pull_images(
            api_object=twitter_api,
            tweet_url="https://twitter.com/thepsf/status/1266007827061116929?lang=en",
        )
        assert bool(images)
        assert len(images) == 1
        assert images.pop() == "http://pbs.twimg.com/media/EZHDaK4XsAE774T.jpg"

    def test_pull_images_no_pic(self, twitter_api):
        # testing pull_images with a tweet with no image.
        images = twitter_api.pull_images(tweet_status)
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


class TestGSearch:
    """Test gsearch module of tweetsourcing.search"""

    def test_kword_search(self):
        # Test the success of connecting to google custom search api
        # and returning a results object
        res = gsearch.kword_search("extracted words OR words OR tweet", 1)
        assert type(res) is dict
        assert bool(res["items"])
        assert bool(res["queries"]["nextPage"][0]["startIndex"])

    def test_categorize_news(self):
        # Test the categorizing a dict into a different news
        # dict based on matches and domain
        tweet_kwords = ["python", "programming", "language"]
        results = {
            "items": [
                {
                    "link": "https://apnews.com/article/florida-python-sniffing-dogs-success-946cadff4d27bdcefb44f1259de6493a",
                    "displayLink": "apnews.com",
                    "title": "Florida's new python-sniffing dogs have 1st success",
                },
                {
                    "link": "https://www.latimes.com/visuals/graphics/la-g-kobe-how-we-did-it-20160419-snap-htmlstory.html",
                    "displayLink": "latimes.com",
                    "title": "How we mapped Kobe's 30,699 shots - Los Angeles Times",
                },
            ],
            "queries": {"nextPage": [{"startIndex": 11}]},
        }
        news = gsearch.categorize_news(results, tweet_kwords)
        assert (
            news["apnews.com"]["title"]
            == "Florida's new python-sniffing dogs have 1st success"
        )
        assert (
            news["apnews.com"]["link"]
            == "https://apnews.com/article/florida-python-sniffing-dogs-success-946cadff4d27bdcefb44f1259de6493a"
        )
        assert news["apnews.com"]["matches"] > 0
        assert news["next_page"] == 11
        del news["next_page"]
        for key, domain in news.items():
            assert (
                domain["title"]
                != "How we mapped Kobe's 30,699 shots - Los Angeles Times"
            )

    def test_extract_articles(self):
        # Test that newspaper3k package still works
        article1 = "https://apnews.com/article/florida-python-sniffing-dogs-success-946cadff4d27bdcefb44f1259de6493a"
        article2 = "https://www.latimes.com/visuals/graphics/la-g-kobe-how-we-did-it-20160419-snap-htmlstory.html"
        kword_gen = gsearch.extract_articles([article1, article2])
        assert bool(kword_gen)
        assert next(kword_gen)
        next(kword_gen)
        with pytest.raises(StopIteration):
            next(kword_gen)
