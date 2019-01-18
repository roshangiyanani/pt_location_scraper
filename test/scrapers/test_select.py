from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.scrapers import Select

path: Path = Path(f'./data/test_files/{Select.company_name}')

test_urls = Select.test_urls

class TestScraperSelectClass(unittest.TestCase):

    def test_get_communities(self):
        with path.joinpath(test_urls['communities'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        urls: [str] = Select._get_communities(page)

    def test_get_clinics(self):
        with path.joinpath(test_urls['locations'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        clinics: [Clinic] = Select._get_clinics(page)
        self.assertEqual(clinics[0], Clinic('Select Physical Therapy', 'Eagle River',
                                            Address.from_address_str('17101 SNOWMOBILE LANE SUITE 202 EAGLE RIVER, AK  99577-7043'),
                                            '(907) 694-8085', 'https://www.selectphysicaltherapy.com/community/alaska/center/?id=40502', fax='(907) 694-8526'))