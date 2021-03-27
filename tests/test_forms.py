import pytest
from tweetsourcing.main.forms import TweetForm


class TestTweetForm:
    """Testing tweet url submission form."""

    def test_validate_url(self, app):
        """Test that an invalid url produces the error."""
        form = TweetForm(tweet_url="Not a URL.")
        assert form.validate() is False
        assert "Please enter in a valid URL" in form.tweet_url.errors