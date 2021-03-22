from google.cloud import vision


def reverse_image_search(uri, full=False, partial=False):
    if full or partial:
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.web_detection(image=image)
        annotations = response.web_detection
        if not annotations.pages_with_matching_images:
            raise Exception('Unable to find matches')
        match_pages = annotations.pages_with_matching_images
        match_pages_urls = [page.url for page in match_pages]
        match_image_urls = []
        partial_match_image_urls = []
        for page in match_pages:
            if full and page.full_matching_images:
                match_image_urls.append(page.full_matching_images[0])
            if partial and page.partial_matching_images:
                partial_match_image_urls.append(page.partial_matching_images[0])
        return match_pages_urls, match_image_urls, partial_match_image_urls
