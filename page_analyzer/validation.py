from urllib.parse import urlparse
import validators


def is_valid(url):
    """Valide url and return bool"""
    return all([validators.url(url),
                url != '',
                len(url) < 255])


def normalize_url(url):
    if is_valid(url):
        parsed_url = urlparse(url)
        normal_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return normal_url
    return False