from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.scrapers import Pivot

path: Path = Path(f'./data/test_files/{Pivot.company_name}')

test_urls = Pivot.test_urls

class TestScraperPivotClass(unittest.TestCase):

    def test_get_states(self):
        with path.joinpath(test_urls['states'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        urls: [str] = Pivot._get_states(page)

    def test_get_locations(self):
        # TODO: update downloader and this to use a file in the test folder for data
        data = {
            'markers': [
                {
                    "id": 408,
                    "name": "INWOOD, WV",
                    "lat": "39.351217",
                    "lng": "-78.02864740000001",
                    "list_format":
'''
                    <tr>\n                            <td><a href=\"https://www.pivotphysicaltherapy.com/locations/inwood/\">INWOOD, WV</a></td>\n                            <td>745 Middleway Pike <br>\n                                Inwood, West Virginia 25428</td>\n                            <td>\n                                Phone 304.229.4141<br>\n                                Fax 304.229.4143\n                            </td>\n                        </tr>'''
                },
            ],
        }
        urls: [str] = Pivot._get_locations(data)
        self.assertEqual(urls[0], 'https://www.pivotphysicaltherapy.com/locations/inwood/')

    def test_get_profile(self):
        with path.joinpath(test_urls['clinic'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        clinic: Clinic = Pivot._get_profile(page, test_urls['clinic'][1])
        self.assertEqual(clinic, Clinic(
            Pivot.company_name, 'INWOOD, WV', Address.from_address_str('Inwood East Plaza 745 Middleway Pike Inwood, WV 25428'),
            '304.229.4141', test_urls['clinic'][1], fax='304.229.4143', email='Inwood@PivotHS.com'
        ))