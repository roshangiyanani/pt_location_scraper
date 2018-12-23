from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.clinic import Clinic
from ptls.scrapers.USPh import USPh

path: Path = Path('./data/test_files')

test_urls = USPh.test_urls

class TestScraperUSPhClass(unittest.TestCase):

    def test_get_states(self):
        with path.joinpath(test_urls['states'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        urls: [str] = USPh._get_states(page)

    def test_get_clinics(self):
        with path.joinpath(test_urls['clinics'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        clinics: [Clinic] = USPh._get_clinics(page, 'TN')
        self.assertEqual(clinics[0], Clinic(USPh.company_name, 'Antioch', 'Antioch, TN'))