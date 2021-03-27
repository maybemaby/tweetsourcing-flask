import os
import pytest
from tweetsourcing import create_app
from tweetsourcing.search.tweethandler import TweetHandler
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def twitter_api(app):
    return TweetHandler(
        api_key=os.environ.get("TWITTER_API_KEY"),
        secret_key=os.environ.get("TWITTER_SECRET_KEY")
    )


@pytest.fixture
def tweet_status(twitter_api):
    return TweetHandler.retrieve_tweet("https://twitter.com/ThePSF/status/1366859617578455041")
