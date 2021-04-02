# TweetSourcing Flask App

Modules used: google-cloud-vision, flask, flask-wtf, google-api-python-client, newspaper3k, pytest, rake-nltk, dotenv

## Usage
```
$ git clone https://github.com/maybemaby/tweetsourcing-flask.git
$ python -m venv tweetsourcing-flask\venv
$ tweetsourcing-flask\venv\Scripts\activate.bat
```

```
$ pip install -e .
$ flask run
```

Fill in secure secret key and valid api credentials to the generated .env file.
Check [here](https://cloud.google.com/vision/docs/before-you-begin) to figure out how to generate the Cloud Vision API json key file and then add it to the .env also.

# Features
- RAKE keyword extraction from tweets
- Google custom news site search engine
- Google Vision API reverse image searches
- Easy to use frontend