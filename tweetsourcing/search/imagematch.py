from collections import namedtuple
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
            raise Exception('Unable to find matches')
        return match_image_urls

#reverse_image_search("https://pbs.twimg.com/media/ExCW_B4WQAQQlVi?format=jpg&name=large", full=True, partial=True)