import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask, current_app
from tweetsourcing.search.tweethandler import TweetHandler
from config import Config


twitter_api = TweetHandler(
    api_key=os.environ.get("TWITTER_API_KEY"),
    secret_key=os.environ.get("TWITTER_SECRET_KEY")
)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    from tweetsourcing.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from tweetsourcing.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/tweetsourcing.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app