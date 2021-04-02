import os
from setuptools import find_packages, setup

if not os.path.exists('.env'):
    with open(".env", "w", encoding="utf-8") as envfile:
        envfile.write('''SECRET_KEY=not-so-secret
FLASK_APP=tweetsourcing
FLASK_ENV=development
TWITTER_API_KEY=
TWITTER_SECRET_KEY=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
CSE_API_KEY=
CSE_ID=
GOOGLE_APPLICATION_CREDENTIALS=''')
        envfile.close()


setup(
    name='tweetsourcing',
    version='1.0.0',
    author='Brandon Ma',
    description='Flask web app for finding secondary sources of tweet info',
    url='https://github.com/maybemaby/tweetsourcing-flask',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-wtf',
        'google-cloud-vision',
        'google-api-python-client',
        'newspaper3k',
        'python-dotenv',
        'rake-nltk',
        'tweepy',
    ],
)