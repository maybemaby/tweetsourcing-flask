import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    FLASK_ENV = os.environ.get("FLASK_ENV") or 'production'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE = os.environ.get("DATABASE_URL") or 'sqlite:///'
    MAX_RESULTS = 30

class TestConfig(object):
    SECRET_KEY = 'not-so-secret'
    DATABASE = 'sqlite:///'
    TESTING = True
    WTF_CSRF_ENABLED = False