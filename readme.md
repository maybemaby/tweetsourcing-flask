# TweetSourcing Flask App

Modules used: google-cloud-vision, flask, flask-wtf, google-api-python-client, newspaper3k, pytest, rake-nltk, dotenv

## Usage
```
$ mkdir tweetsourcing-flask
$ python -m venv tweetsourcing-flask\venv
$ tweetsourcing\venv\Scripts\activate.bat
```

```
git clone https://github.com/maybemaby/tweetsourcing-flask.git
pip install -e
```

Fill in secure secret key and valid api credentials to the generated .env file.

# Features
- RAKE keyword extraction from tweets
- Google custom news site search engine
- Google Vision API reverse image searches
- Easy to use frontend