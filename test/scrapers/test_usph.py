from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.scrapers.USPh import USPh

path: Path = Path(f'./data/test_files/{USPh.company_name}')

test_urls = USPh.test_urls

class TestScraperUSPhClass(unittest.TestCase):

    def test_get_states(self):
        with path.joinpath(test_urls['states'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        urls: [str] = USPh._get_states(page)

    def test_get_clinics(self):
        with path.joinpath(test_urls['clinics'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        clinics: [Clinic] = USPh._get_clinics(page, 'NJ')
        self.assertEqual(clinics[0], Clinic(USPh.company_name, 'Boonton',
                                            Address.from_city_state('Boonton', 'NJ')))