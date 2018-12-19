import unittest

from ptls.clinic import Clinic
from ptls.scrapers.athletico import get_states_location_urls, get_state_location_urls, get_location_info

scraper_test_loc: str = './test/scrapers/test_files'
# scraper_test_loc: str = './test_files'

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
        # print(urls)

    def test_get_location(self):
        with open(f'{scraper_test_loc}/athletico/bloomington.html', 'rb') as f:
            raw_html: str = f.read()
        clinic: Clinic = get_location_info(raw_html, f'{scraper_test_loc}/athletico/bloomington.html')
        # print(clinic)
        self.assertEqual(clinic,
                         Clinic('Athletico Physical Therapy', 'Bloomington',
                                'Bloomington 1704 Eastland Dr., Unit 15 Bloomington, IL 61704',
                                '309-664-7766', f'{scraper_test_loc}/athletico/bloomington.html',
                                fax='309-664-6767', email='BloomingtonIL@athletico.com'))