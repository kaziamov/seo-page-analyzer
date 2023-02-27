import requests
import bs4


def get_data(url):
    """Make request to url and return responce

    Args:
        url (str):

    Returns:
        requests.Responce
    """
    try:
        responce = requests.get(url)
    except requests.exceptions.ConnectionError:
        return False
    return parse_data(responce)


def parse_data(data):
    """Parse status code, title, h1 and description from responce
    and return tuple.

    Args:
        data (requests.Responce):

    Returns:
        tuple
    """
    html = bs4.BeautifulSoup(data.text)
    status = data.status_code
    title = html.title
    h1 = html.find('h1')
    desc = html.find("meta", attrs={'name': 'description'})
    return (status,
            title.string if title else '',
            h1.get_text() if h1 else '',
            desc['content'] if desc else '')
