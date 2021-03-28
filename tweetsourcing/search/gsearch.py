import os
from collections import namedtuple
from flask import current_app
from newspaper import Article, news_pool
from newspaper.utils import memoize_articles
from rake_nltk import Rake
from googleapiclient.discovery import build

# TODO: Put full titles in news

def kword_search(query:str, startnum:int, orTerms:list=None):
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
    if orTerms:
        res = (
            service.cse().siterestrict()
            .list(q=query, cx=os.environ.get("CSE_ID"), lr="lang_en", orTerms=orTerms, start=startnum)
            .execute()
    )
    else:
        res = (
            service.cse().siterestrict()
            .list(q=query, cx=os.environ.get("CSE_ID"), lr="lang_en", start=startnum)
            .execute()
        )
    return res


def categorize_news(results_object: dict, tweet_kwords: list, *args):
    """Categorizes search results with most matches
    based on the news source they came from.

    Inputs
    ------
    Google search results object
    Keyword list from tweet
    optional: Existing news dict.
    Returns
    --------
    Nested dictionary for each news source with the title
    and link to the article with the most keyword matches.
    """
    # result_items is the items entity in the JSON google search returns
    try:
        result_items = results_object["items"]
    except KeyError:
        current_app.logger.error(
            f'''No results found for search: {results_object["queries"]["request"][0]["searchTerms"]}'''
            )
    # getting the next page int from the JSON
    next_page = results_object["queries"].get("nextPage",None)
    if next_page:
        next_page = next_page[0]["startIndex"]
    if len(args) > 0:
        news = args[0]
    else:
        news = {
            "apnews.com": {"title": "", "link": "", "matches": 0},
            "abcnews.go.com": {"title": "", "link": "", "matches": 0},
            "www.cnn.com": {"title": "", "link": "", "matches": 0},
            "www.foxnews.com": {"title": "", "link": "", "matches": 0},
            "www.msnbc.com": {"title": "", "link": "", "matches": 0},
            "www.nationalreview.com": {"title": "", "link": "", "matches": 0},
            "www.nytimes.com": {"title": "", "link": "", "matches": 0},
            "www.reuters.com": {"title": "", "link": "", "matches": 0},
            "www.theepochtimes.com": {"title": "", "link": "", "matches": 0},
            "www.washingtonpost.com": {"title": "", "link": "", "matches": 0},
        }
        # comprehension breakdown: if article site in news dict, add a Result namedtuple with link, title and website attrs to list
        Result = namedtuple("Result", ["link", "site", "title"])
        article_results = [
            Result(item["link"], item["displayLink"], item["title"])
            for item in result_items
            if item["displayLink"] in news
        ]
        article_kword_gen = extract_articles([article.link for article in article_results])
        for result in article_results:
            try:
                article_kwords, article_title = next(article_kword_gen) 
                kword_matches = keyword_compare(tweet_kwords, article_kwords)
            except TypeError:
                continue
            if kword_matches > news[result.site]["matches"]:
                news[result.site]["title"] = article_title
                news[result.site]["link"] = result.link
                news[result.site]["matches"] = kword_matches
    news["next_page"] = next_page
    return news


def extract_articles(url_list):
    """Extracts article text and keywords from url.

    Inputs
    ------
    url_list: list
    Returns
    -------
    generator with keywords parsed from article url list
    """
    articles = [Article(url, memoize_articles=True, fetch_images=False) for url in url_list]
    news_pool.set(articles)
    news_pool.join()
    r = Rake()
    for article in articles:
        article.parse()
        r.extract_keywords_from_text(article.text)
        article_kwords = r.get_ranked_phrases()
        if article_kwords:
            yield article_kwords, article.title
        else:
            yield None


def keyword_compare(kwords1:list, kwords2:list):
    """Counts matches of keywords in kwords1 to
    keywords in kwords2.

    Inputs
    ------
    list kwords1: Keywords to search for within kwords2.
    list kwords2: Keywords to search from.
    Returns
    -------
    float matches: number of times keyword in kwords1 shows up in kwords2.
    """
    if type(kwords2) != list or len(kwords2) == 0:
        raise TypeError(f'keyword_compare only takes an iterable list of words, {repr(kwords2)} is not compatible')
    matches = 0
    for kword in set(kwords1):
        match_list = [match for match in set(kwords2) if kword in match]
        matches += len(match_list)
    return matches / len(kwords2)

    
def search_helper(query:str, startnum:int=1,*args, **kwargs) -> dict:
    """Ties the kword_search, categorize_news, and keyword_compare functions together
    from this module.

    :param query: Query string to google search
    :type query: str
    :param startnum: Page of google search results to start on, defaults to 1
    :type startnum: int, optional
    :return: nested dict of news domains with their highest matching articles
    :rtype: dict
    """
    startnum = startnum
    while int(startnum) <= current_app.config['MAX_RESULTS']:
        if kwargs['orTerms']:
            results = kword_search(query,startnum, orTerms=kwargs['orTerms'])
        else:
            results = kword_search(query, startnum)
        try:
            news_dict = categorize_news(results, kwargs['tweet_kwords'], news_dict)
        except:
            news_dict = categorize_news(results, kwargs['tweet_kwords'])
        for domain in news_dict.values():
            if domain["title"] == "":
                startnum = news_dict["next_page"]
                break
    news_dict.pop("next_page")
    return news_dict
