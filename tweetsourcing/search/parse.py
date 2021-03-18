from rake_nltk import Rake


def extract_kwords(tweet_object: "tweepy.Status") -> list:
    """Uses RAKE algorithm to extract keywords from a tweet.

    :param tweet_object: Tweepy Status object generated from url
    :type tweet_object: tweepy.Status
    :return: [description]
    :rtype: [type]
    """
    r = Rake()
    tweet_text = tweet_object.full_text
    r.extract_keywords_from_text(tweet_text)
    return r.get_ranked_phrases()


def create_query(kword_list):
    """Takes keyword list and joins them to be used in google search."""
    query = " OR ".join(kword_list)
    return query


def query_from_parse(tweet_object: "tweepy.Status") -> str:
    """Helper function to tie together create_query and extract_kwords"""
    return create_query(extract_kwords(tweet_object))
