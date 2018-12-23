from bs4 import BeautifulSoup
import re
import sys
from typing import Dict, Iterator, Tuple

from ptls.clinic import Clinic
from ptls.requester import Requester

states_url: str = 'http://usph.com/corporate/clinic-locations.aspx'

state_regex: re.Match = re.compile(r'\?state=([a-zA-Z][a-zA-Z])')

class USPh:
    company_name = 'USPh'
    company_name_upper = company_name.upper()

    @staticmethod
    def run(req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{USPh.company_name_upper}: Processing.')
        total_location_count: int = 0

        states: [(str, str)] = USPh._get_states(req.get_page_bs(states_url))
        states_len: int = len(states)
        state_count: int = 0
        for (state_url, state) in states:
            state_count = state_count + 1
            sys.stdout.write(f'\r{USPh.company_name_upper}: Processing state {state_count}/{states_len}.')

            locations: [Clinic] = USPh._get_clinics(req.get_page_bs(state_url), state)
            total_location_count = total_location_count + len(locations)
            for clinic in locations:
                yield clinic

        sys.stdout.write(f'\r{USPh.company_name_upper}: Processed {states_len} states to find {total_location_count} clinics.\n')
    
    @staticmethod
    def _get_states(page: BeautifulSoup) -> [(str, str)]:
        urls: [str] = list()
        for link in page.find('map').find_all('area'):
            link_address: str = link.get('href')
            url: str = f'{states_url}{link_address}'
            state: str = state_regex.match(link_address)[1].upper()
            urls.append((url, state))
        return urls

    @staticmethod
    def _get_clinics(page: BeautifulSoup, state: str) -> [Clinic]:
        locations: [Clinic] = list()
        for td in page.find(id='UpdatePanel1').find('td').find_all('td')[1:]:
            # TODO: find better way of getting first item in generator
            city: str = td.stripped_strings.__next__().strip()
            address: str = f'{city}, {state}'
            clinic: Clinic = Clinic(USPh.company_name, city, address)
            locations.append(clinic)
        return locations

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'states': (f'{company_name}/locations.html', states_url),
        'clinics': (f'{company_name}/tn.html', f'{states_url}?state=tn#top'),
    })