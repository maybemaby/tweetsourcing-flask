import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'not-so-secret'
    DATABASE = os.environ.get("DATABASE_URL") or 'sqlite:///'

class TestConfig(object):
    SECRET_KEY = 'not-so-secret'
    DATABASE = os.environ.get("DATABASE_URL") or 'sqlite:///'
    TESTING = True