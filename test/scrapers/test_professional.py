from bs4 import BeautifulSoup
from pathlib import Path
import unittest

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.scrapers import Professional

path: Path = Path(f'./data/test_files/{Professional.company_name}')

test_urls = Professional.test_urls

class TestScraperProfessionalClass(unittest.TestCase):

    def test_get_communities(self):
        with path.joinpath(test_urls['communities'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        urls = Professional._get_communities(page)

    def test_get_clinics(self):
        with path.joinpath(test_urls['profile'][0]).open('rb') as f:
            raw_html: str = f.read()
        page: BeautifulSoup = BeautifulSoup(raw_html, 'lxml')
        clinic: Clinic = Professional._get_clinic(page, 'https://www.professionalpt.com/office/broad-street/')
        self.assertEqual(clinic, Clinic(Professional.company_name, 'Broad Street',
                                        Address.from_address_str('30 Broad Street, 12th Floor (at Exchange Pl.) New York, NY 10004'),
                                        '212-587-8606',
                                        'https://www.professionalpt.com/office/broad-street/',
                                        fax='212-587-9024'))