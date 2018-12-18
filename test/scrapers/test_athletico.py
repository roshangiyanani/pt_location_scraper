import unittest

from ptls.scrapers.athletico import get_states_location_urls, get_state_location_urls

scraper_test_loc: str = './test/scrapers/test_files'

class TestScraperAthleticoClass(unittest.TestCase):

    # def test_get_states_location_page(self):
    #     get_states_location_urls()

    def test_get_states_location_url(self):
        with open(f'{scraper_test_loc}/athletico/locations.html', 'rb') as f:
            raw_html: str = f.read()
        urls: [str] = get_states_location_urls(raw_html)
        # print(urls)

    def test_get_state_location_urls(self):
        with open(f'{scraper_test_loc}/athletico/illinois.html', 'rb') as f:
            raw_html: str = f.read()
        urls: [str] = get_state_location_urls(raw_html)