# from urllib.parse import urlparse
import validators


def is_valid(data):
    """Valide url and return bool

    Args:
        data (str): url

    Returns:
        bool
    """
    # checker = urlparse(data)
    # return all([checker.scheme, checker.netloc, len(data) < 255])
    return all([validators.url(data), len(data) < 255])
