    """imagematch is for taking an image url and passing it to the google vision api
    to return a list of urls and titles for web pages with matching images.
    """
from collections import namedtuple
from flask.globals import current_app
from google.cloud import vision


def reverse_image_search(uri:str, full:bool=False) -> tuple:
    if full:
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.web_detection(image=image)
        annotations = response.web_detection
        pages = annotations.pages_with_matching_images
        ImagePage = namedtuple("Imagepage", ["url", "title"])
        if full:
            match_image_urls = [ImagePage(page.url, page.page_title) for page in pages if page.full_matching_images]
        else:
            match_image_urls = []
            partial_match_image_urls = []
        if len(match_image_urls) == 0:
            current_app.loggers.warning(f'No matches found for url: {uri}')
            raise Exception('Unable to find matches')
        return match_image_urls