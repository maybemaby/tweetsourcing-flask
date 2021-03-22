from collections import namedtuple
from google.cloud import vision


def reverse_image_search(uri:str, full:bool=False, partial:bool=False) -> tuple:
    if full or partial:
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.web_detection(image=image)
        annotations = response.web_detection
        URLSet = namedtuple("URLSet", ["full", "partial"])
        if full:
            match_image_urls = [image.url for image in annotations.full_matching_images]
        else:
            match_image_urls = []
        if partial:
            partial_match_image_urls =[image.url for image in annotations.visually_similar_images]
        else:
            partial_match_image_urls = []
        if len(match_image_urls) == 0 and len(partial_match_image_urls) == 0:
            raise Exception('Unable to find matches')
        return URLSet(match_image_urls, partial_match_image_urls)
