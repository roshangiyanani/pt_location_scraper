from bs4 import BeautifulSoup
import re
from re import Match
import sys
from typing import Dict, Iterator, Tuple

from ptls.clinic import Clinic
from ptls.requester import Requester

regionMatch = re.compile('/region/*')
locationMatch = re.compile('/locations/*')
phoneMatch = re.compile('(tel:)(.*)')
emailMatch = re.compile('(mailto:)(.*)')

base_url: str = 'https://www.athletico.com'
states_url: str = f'{base_url}/locations/'


class Athletico:
    @staticmethod
    def run(req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\rATHLETICA: Processing.')
        total_location_count: int = 0

        states: [str] = Athletico._get_states(req, states_url)
        # print(states)
        states_len: int = len(states)
        state_count: int = 0
        for state_url in states:
            state_count = state_count + 1
            sys.stdout.write(
                f'\rATHLETICA: Processing state {state_count}/{states_len}.                      ')

            locations: [str] = Athletico._get_locations(req, state_url)
            # print(locations)
            locations_len: int = len(locations)
            location_count: int = 0
            for location_url in locations:
                location_count = location_count + 1
                sys.stdout.write(
                    f'\rATHLETICA: Processing state {state_count}/{states_len} and location {location_count}/{locations_len}.              ')
                yield Athletico._get_clinic(req, location_url)
            total_location_count = total_location_count + location_count

        sys.stdout.write(
            f'\rATHLETICA: Processed {states_len} states to find {total_location_count} clinics.                \n')

    @staticmethod
    def _get_states(req: Requester, url: str) -> [str]:
        raw_html: str = req.get_page_str(url)
        return Athletico._get_states_urls(raw_html)

    @staticmethod
    def _get_states_urls(raw_html: str) -> [str]:
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        urls: [str] = list()
        for link in page.find(id='awardsTiles').find_all('a'):
            # print(link)
            link_address: str = link.get('href')
            if regionMatch.match(link_address) is not None \
                    and link_address != '/regions/view-our-national-location-list/':
                urls.append(f'{base_url}{link_address}')
        return urls

    @staticmethod
    def _get_locations(req: Requester, url: str) -> [str]:
        raw_html: str = req.get_page_str(url)
        return Athletico._get_location_urls(raw_html)

    @staticmethod
    def _get_location_urls(raw_html: str) -> [str]:
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        urls: [str] = list()
        for link in page.find('div', {'class': 'pf-content'}).find_all('a'):
            link_address: str = link.get('href')
            if locationMatch.match(link_address) is not None:
                urls.append(f'{base_url}{link_address}')
        return urls

    @staticmethod
    def _get_clinic(req: Requester, url) -> Clinic:
        raw_html: str = req.get_page_str(url)
        return Athletico._get_clinic_info(raw_html, url)

    @staticmethod
    def _get_clinic_info(raw_html: str, url: str) -> Clinic:
        page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        company: str = 'Athletico Physical Therapy'
        location_name: str = page.find('h1', {'class': 'innerPage'}).string
        address: str = ' '.join(page.find('div', id='geographicInfo')
                                .find('p', {'class': 'subheadText'}).stripped_strings)
        phone = None
        email = None
        for link in page.find('div', id='contactInfo').find_all('a'):
            link_address: str | None = link.get('href')
            if link_address is not None:
                phone_match: Match = phoneMatch.match(link_address)
                email_match: Match = emailMatch.match(link_address)
                if phone_match is not None:
                    phone: str = phone_match[2].strip()
                elif email_match is not None:
                    email: str = email_match[2].strip()
        fax: str = page.find('div', id='contactInfo').find(
            'div').find('span').string
        return Clinic(company, location_name, address, phone, url, fax, email)

test_urls: Dict[str, Tuple[str, str]] = dict({
    'states': ('athletico/locations.html', states_url),
    'locations': ('athletico/illinois.html', 'http://www.athletico.com/regions/illinois/'),
    'clinic': ('athletico/bloomington.html', 'http://www.athletico.com/locations/bloomington-illinois/?location=bloomington-illinois'),
})