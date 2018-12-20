from requests import get, Response
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time

class Requester:
    """
    Manages all requests and ensures we do not make too many requests at once by measuring the time between calls
    and sleeping if necessary.
    """
    _min_delay: int  # stored as nanoseconds
    _last_use: int

    def __init__(self, min_delay: float):
        """
        Initializes the requester class.
        :param min_delay: seconds between requests
        """
        self._min_delay = min_delay * 10**9
        self._set_last_use()

    def _set_last_use(self):
        """
        Updates the last use to now.
        :return:
        """
        self._last_use = time.perf_counter_ns()

    def _ensure_delay(self):
        """
        Delays the function until the function call is complete.
        :return: None
        """
        current_time: int = time.perf_counter_ns()
        delta: int = current_time - self._last_use
        # print(f'current({current_time}) - last_use({self._last_use}) = delta({delta})')
        if delta < self._min_delay:
            sleep_time: float = (self._min_delay - delta) / 10**9
            # print(f'sleeping for {sleep_time} seconds')
            time.sleep(sleep_time)
        self._set_last_use()

    def get_page_str(self, url: str) -> str or None:
        self._ensure_delay()
        retval: str or None = Requester._get_page_str(url)
        return retval

    def get_page_bs(self, url: str) -> BeautifulSoup or None:
        self._ensure_delay()
        retval: BeautifulSoup or None = Requester._get_page_bs(url)
        return retval

    @staticmethod
    def log_error(e: str):
        print(e)

    @staticmethod
    def _get_page_str(url: str) -> str or None:
        """
            Attempts to get the content at `url` by making an HTTP GET request.
            If the content-type of response is some kind of HTML/XML, return the
            text content, otherwise return None.
            :param url: URL to download
            :return: raw string of contents
            """
        try:
            with get(url, stream=True) as resp:
                if Requester.is_good_response(resp):
                    raw_html: str = resp.content
                    return raw_html
                else:
                    return None
        except RequestException as e:
            Requester.log_error(f'Error during requests to {url} : {str(e)}')
            return None

    @staticmethod
    def _get_page_bs(url) -> BeautifulSoup or None:
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        :param url: URL to download
        :return: BeautifulSoup object of contents
        """
        raw_html: str or None = Requester._get_page_str(url)
        if raw_html is not None:
            return BeautifulSoup(raw_html, 'html.parser')
        else:
            return None


    @staticmethod
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