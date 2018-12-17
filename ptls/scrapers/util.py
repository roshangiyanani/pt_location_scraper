from bs4 import BeautifulSoup
from requests import get, Response
from requests.exceptions import RequestException

def get_page(url) -> None or BeautifulSoup:
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    :param url: URL to download
    :return: BeautifulSoup object of contents
    """
    try:
        with get(url, stream=True) as resp:
            if is_good_response(resp):
                raw_html: str = resp.content
                return BeautifulSoup(raw_html, 'html.parser')
            else:
                return None
    except RequestException as e:
        log_error(f'Error during requests to {url} : {str(e)}')


def is_good_response(resp: Response) -> bool:
    """
    Return true if the response seems to be HTML, False otherwise.
    :param resp:
    :return:
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e: str):
    print(e)