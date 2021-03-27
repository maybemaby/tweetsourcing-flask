import pytest
from tweetsourcing.main.forms import TweetForm, SearchForm


class TestTweetForm:
    """Testing tweet url submission form."""

    def test_validate_url(self, app):
        """Test that an invalid url produces the error."""
        form = TweetForm(tweet_url="Not a URL.")
        assert form.validate() is False
        assert "Please enter in a valid URL" in form.tweet_url.errors

    def test_validate_pass(self, app):
        """Test that a twitter url passes validation."""
        form = TweetForm(tweet_url="https://twitter.com/ThePSF/status/1366859617578455041")
        assert form.validate() is True

class TestSearchForm:
    """Testing query submission form."""

    def test_query_too_long(self,app):
        form = SearchForm(query="11"*141, or_terms="testing|in|pytest"*100, img_search=False)
        assert form.validate() is False
        assert "Query too long" in form.query.errors
        assert "Additional terms too long" in form.or_terms.errors

    def test_validate_success(self, app):
        form = SearchForm(query="Python releases 3.9", or_terms="Guido|programming|language|new features", img_search=True)
        assert form.validate() is True