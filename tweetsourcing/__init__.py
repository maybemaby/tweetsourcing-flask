import os

from flask import Flask, current_app
from tweepy import API as TwitterAPI
from tweepy import AppAuthHandler
from config import Config


auth = AppAuthHandler(
    consumer_key=os.environ.get("TWITTER_API_KEY"),
    consumer_secret=os.environ.get("TWITTER_SECRET_KEY"),
)
twitter_api = TwitterAPI(auth)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    from tweetsourcing.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from tweetsourcing.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app