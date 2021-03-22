from google.cloud import vision


def reverse_image_search(uri, full=False, partial=False):
    if full or partial:
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.web_detection(image=image)
        annotations = response.web_detection
        if full:
            match_image_urls = annotations.full_matching_images
        else:
            match_image_urls = []
        if partial:
            partial_match_image_urls = annotations.visually_similar_images
        else:
            partial_match_image_urls = []
        if len(match_image_urls) == 0 and len(partial_match_image_urls) == 0:
            raise Exception('Unable to find matches')
        return match_image_urls, partial_match_image_urls
