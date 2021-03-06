"""parse is the module for functions that parse information from tweets
and do something directly with the parsed info.
"""

from rake_nltk import Rake


def extract_kwords(tweet_text: str) -> list:
    """Uses RAKE algorithm to extract keywords from a tweet.

    :param tweet_object: Tweepy Status object generated from url
    :type tweet_object: tweepy.Status
    :return: [description]
    :rtype: [type]
    """
    r = Rake()
    r.stopwords += ["https", "http", "https://", "https ://" "http://", "://", "www"]
    r.extract_keywords_from_text(tweet_text)
    return r.get_ranked_phrases()


def create_query(kword_list):
    """Takes keyword list and returns them as a main query and additional terms
    used for the google custom search orTerms parameter."""
    # filter out possible unnecessary words
    kword_list = [word for word in kword_list if len(word) > 2]
    query = kword_list[0]
    if len(kword_list) > 1:
        or_terms = "|".join(kword_list[1:])
        return query, or_terms
    return query


def query_from_parse(tweet_text: str) -> str:
    """Helper function to tie together create_query and extract_kwords"""
    kwords = extract_kwords(tweet_text)
    return create_query(kwords)
