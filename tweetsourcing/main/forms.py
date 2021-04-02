import re
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms.fields import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length, URL, ValidationError


def twitter_url_check(form, field):
    """Custom validator for ensuring URL is twitter link."""
    tweet_regex = re.compile(r"(.+/status/\d+)(\?s=\d+)?", flags=re.IGNORECASE)
    tweet_mo = re.search(tweet_regex, field.data)
    if not tweet_mo:
        raise ValidationError("Must be a Tweet Status URL")


class TweetForm(FlaskForm):
    tweet_url = URLField(
        "Enter a tweet URL",
        validators=[
            DataRequired(message="Please fill in a valid URL"),
            URL(message="Please enter in a valid URL"),
            twitter_url_check,
        ],
    )
    submit = SubmitField("Find Sources")


class SearchForm(FlaskForm):
    query = StringField(validators=[Length(max=141, message="Query too long")])
    or_terms = StringField(
        validators=[Length(max=141, message="Additional terms too long")]
    )
    img_search = BooleanField(
        label="Reverse Image Search", default=False, id="img_search"
    )
    submit = SubmitField("Confirm")
