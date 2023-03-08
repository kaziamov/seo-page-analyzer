from urllib.parse import urlparse


def is_valid(data):
    """Valide url and return bool

    Args:
        data (str): url

    Returns:
        bool
    """
    checker = urlparse(data)
    return all([checker.scheme, checker.netloc, checker.path, len(data) < 255])
