import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABSE = os.path.join(app.instance_path, 'tweetsourcing.sqlite')