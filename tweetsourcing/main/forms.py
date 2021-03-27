from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms.fields import SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Length, URL


class TweetForm(FlaskForm):
    tweet_url = URLField(
        "Enter a tweet URL",
        validators=[DataRequired(message="Please fill in a valid URL"), URL(message="Please enter in a valid URL")],
    )
    submit = SubmitField('Find Sources')

class SearchForm(FlaskForm):
    query = StringField(validators=[Length(max=141, message="Query too long")])
    or_terms = StringField(validators=[Length(max=141, message="Additional terms too long")])
    img_search = BooleanField(label="Reverse Image Search", default=False)
    submit = SubmitField('Confirm')