from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.clinic import Clinic
from ptls.scrapers.ATI import ATI, test_urls

path: Path = Path('./data/test_files')

class TestScraperATIClass(unittest.TestCase):

    def test_get_states(self):
        with path.joinpath(test_urls['states'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        urls: [str] = ATI._get_states(page)

    def test_get_location(self):
        with path.joinpath(test_urls['locations'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        urls: [str] = ATI._get_location(page)

    def test_get_clinics(self):
        with path.joinpath(test_urls['clinics'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        urls: [(str, str)] = ATI._get_clinics(page)

    def test_parse_profile(self):
        with path.joinpath(test_urls['profile'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        clinic: Clinic = ATI._parse_profile(page, 'Fairbanks - Lathrop St', test_urls['profile'][0])
        # TODO: Fix 'Fairbanks ,' spacing
        self.assertEqual(clinic, Clinic(
            'ATI Physical Therapy', 'Fairbanks - Lathrop St',
            '1919 Lathrop St, #123, Fairbanks , AK 99701',
            '(907) 455-4401', test_urls['profile'][0],
            fax='(907) 455-4402'
        ))
