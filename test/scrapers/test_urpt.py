from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.scrapers import URPT

path: Path = Path(f'./data/test_files/{URPT.company_name}')

test_urls = URPT.test_urls

class TestScraperURPTClass(unittest.TestCase):

    def test_get_data(self):
        with path.joinpath(test_urls['all'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        data = URPT._get_data(page)

    def test_get_clinics(self):
        with path.joinpath(test_urls['all'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        data = URPT._get_data(page)
        clinic: Clinic = URPT._get_clinic(data[0])
        self.assertEqual(clinic, Clinic('Drayer Physical Therapy Institute', 'Alabaster',
            Address.from_address_str('831 1st Street North, Suite B, Alabaster, AL 35007-8944'), '205-358-9138', 'https://drayerpt.com/locations/alabaster/', fax='205-358-9139'))