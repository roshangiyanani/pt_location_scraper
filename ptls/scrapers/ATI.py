from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.clinic import Clinic
from ptls.requester import Requester

states_url: str = 'https://locations.atipt.com'

test_urls: Dict[str, Tuple[str, str]] = dict({
    'states': ('ati/locations.html', states_url),
    'locations': ('ati/ma.html', 'https://locations.atipt.com/ma'),
    'clinics': ('ati/fairbanks.html', 'https://locations.atipt.com/ak/fairbanks'),
    'profile': ('ati/fairbanks-ak.html', 'https://locations.atipt.com/fairbanks-ak'),
})

class ATI:

    @staticmethod
    def run(req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\rATI: Processing.')
        total_location_count: int = 0

        states: [str] = ATI._get_states(req.get_page_bs(states_url))
        states_len: int = len(states)
        state_count: int = 0
        for state_url in states:
            state_count = state_count + 1
            sys.stdout.write(f'\rATI: Processing state {state_count}/{states_len}.')

            locations: [str] = ATI._get_location(req.get_page_bs(state_url))
            locations_len: int = len(locations)
            total_location_count = total_location_count + locations_len
            location_count: int = 0
            for location_url in locations:
                location_count = location_count + 1
                sys.stdout.write(f'\rATI: Processing state {state_count}/{states_len} and location {location_count}/{locations_len}.')

                profiles: [(str, str)] = ATI._get_clinics(req.get_page_bs(location_url))
                for (profile_url, name) in profiles:
                    yield ATI._parse_profile(req.get_page_bs(profile_url), name, profile_url)

        sys.stdout.write(f'\rATI: Processed {states_len} states to find {total_location_count} clinics.\n')

    @staticmethod
    def _get_states(page: BeautifulSoup) -> [str]:
        urls: [str] = list()
        for link in page.find('div', {'class': 'location-drilldown-list'}).find_all('a'):
            link_address: str = link.get('href')
            urls.append(f'{states_url}{link_address}')
        return urls

    @staticmethod
    def _get_location(page: BeautifulSoup) -> [str]:
        return ATI._get_states(page)  # has same format

    @staticmethod
    def _get_clinics(page: BeautifulSoup) -> [(str, str)]:
        clinics: [(str, str)] = list()
        for listing in page.find_all('div', {'class': 'listing'}):
            link = listing.find('a')
            link_address: str = link.get('href')
            name: str = link.string.strip()
            clinics.append((f'{states_url}{link_address}', name))
        return clinics

    @staticmethod
    def _parse_profile(page: BeautifulSoup, name: str, url: str) -> Clinic:
        info = page.find('div', id='business-info')
        address: str = ' '.join(info.find('div').stripped_strings)
        phone: str = info.find('div', {'class': 'desktop'}).find('span').string.strip()
        fax: str = info.contents[9].string.strip()[4:].strip()
        clinic: Clinic = Clinic('ATI Physical Therapy', name, address, phone, url, fax=fax)
        return clinic