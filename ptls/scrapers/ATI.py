from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class ATI:

    base_url: str = 'https://locations.atipt.com'

    company_name = 'ATI'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'states': (f'locations.html', base_url),
        'locations': (f'ma.html', f'{base_url}/ma'),
        'clinics': (f'fairbanks.html', f'{base_url}/ak/fairbanks'),
        'profile': (f'fairbanks-ak.html', f'{base_url}/fairbanks-ak'),
    })

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')
        total_location_count: int = 0

        states: [str] = cls._get_states(req.get_page_bs(cls.base_url))
        states_len: int = len(states)
        state_count: int = 0
        for state_url in states:
            state_count = state_count + 1
            sys.stdout.write(f'\r{cls.company_name_upper}: Processing state {state_count}/{states_len}.')

            locations: [str] = cls._get_location(req.get_page_bs(state_url))
            locations_len: int = len(locations)
            total_location_count = total_location_count + locations_len
            location_count: int = 0
            for location_url in locations:
                location_count = location_count + 1
                sys.stdout.write(f'\r{cls.company_name_upper}: Processing state {state_count}/{states_len} and location {location_count}/{locations_len}.')

                profiles: [(str, str)] = cls._get_clinics(req.get_page_bs(location_url))
                for (profile_url, name) in profiles:
                    yield cls._parse_profile(req.get_page_bs(profile_url), name, profile_url)

        sys.stdout.write(f'\r{cls.company_name_upper}: Processed {states_len} states to find {total_location_count} clinics.\n')

    @classmethod
    def _get_states(cls, page: BeautifulSoup) -> [str]:
        urls: [str] = list()
        for link in page.find('div', {'class': 'location-drilldown-list'}).find_all('a'):
            link_address: str = link.get('href')
            urls.append(f'{cls.base_url}{link_address}')
        return urls

    @classmethod
    def _get_location(cls, page: BeautifulSoup) -> [str]:
        return cls._get_states(page)  # has same format

    @classmethod
    def _get_clinics(cls, page: BeautifulSoup) -> [(str, str)]:
        clinics: [(str, str)] = list()
        for listing in page.find_all('div', {'class': 'listing'}):
            link = listing.find('a')
            link_address: str = link.get('href')
            name: str = link.string.strip()
            clinics.append((f'{cls.base_url}{link_address}', name))
        return clinics

    @classmethod
    def _parse_profile(cls, page: BeautifulSoup, name: str, url: str) -> Clinic:
        info = page.find('div', id='business-info')
        address: Address = Address.from_address_str(' '.join(info.find('div').stripped_strings))
        phone: str = info.find('div', {'class': 'desktop'}).find('span').string.strip()
        fax: str = info.contents[9].string.strip()[4:].strip()
        clinic: Clinic = Clinic(cls.company_name, name, address, phone, url, fax=fax)
        return clinic