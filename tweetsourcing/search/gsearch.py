import os
from newspaper import Article, news_pool
from rake_nltk import Rake
from googleapiclient.discovery import build


def kword_search(query, startnum):
    """Performs google customsearch.

    Inputs
    -------
    str: query (list of keywords)
    int: Starting search result index
    Returns
    -------
    google customsearch Results object.
    """
    service = build("customsearch", "v1", developerKey=os.environ.get("CSE_API_KEY"))
    res = (
        service.cse()
        .list(q=query, cx=os.environ.get("CSE_ID"), lr="lang_en", start=startnum)
        .execute()
    )
    return res


