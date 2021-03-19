import os
import pytest
from tweetsourcing import create_app
import tweetsourcing.search.tweethandler


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def twitter_api(app):
    return tweetsourcing.search.tweethandler.create_api()


@pytest.fixture
def tweet_status(twitter_api):
    return tweetsourcing.search.tweethandler.retrieve_tweet(
        twitter_api, "https://twitter.com/ThePSF/status/1366859617578455041"
    )
