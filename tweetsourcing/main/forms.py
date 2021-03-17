from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, URL


class TweetForm(FlaskForm):
    tweet_url = URLField(
        "Enter a tweet URL",
        validators=[DataRequired(), URL(message="Please enter in a valid URL")],
    )
    submit = SubmitField('Find Sources')
