from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import DataRequired, Length, URL


class TweetForm(FlaskForm):
    tweet_url = URLField(
        "Enter a tweet URL",
        validators=[DataRequired(), URL(message="Please enter in a valid URL")],
    )
    submit = SubmitField('Find Sources')

class SearchForm(FlaskForm):
    query = StringField(validators=[Length(max=141, message="Query too long")])
    submit = SubmitField('Confirm')