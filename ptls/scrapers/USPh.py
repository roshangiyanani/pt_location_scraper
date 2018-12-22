from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.clinic import Clinic
from ptls.requester import Requester

states_url: str = 'http://usph.com/corporate/clinic-locations.aspx'

class USPh:
    company_name = 'USPh'
    company_name_upper = company_name.upper()

    @staticmethod
    def run(req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{USPh.company_name_upper}: Processing.')
        total_location_count: int = 0

        states: [str] = USPh._get_states(req.get_page_bs(states_url))
        states_len: int = len(states)
        state_count: int = 0
        for state_url in states:
            state_count = state_count + 1
            sys.stdout.write(f'\r{USPh.company_name_upper}: Processing state {state_count}/{states_len}.')

            locations: [str] = list()  # TODO
            locations_len: int = len(locations)
            total_location_count = total_location_count + locations_len
            location_count: int = 0
            # TODO go through locations

        sys.stdout.write(f'\r{USPh.company_name_upper}: Processed {states_len} states to find {total_location_count} clinics.\n')
        yield Clinic('USPh', 'test', 'test')
    
    @staticmethod
    def _get_states(page: BeautifulSoup) -> [str]:
        urls: [str] = list()
        for link in page.find('map').find_all('area'):
            link_address: str = link.get('href')
            urls.append(f'{states_url}{link_address}')
        return urls

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'states': (f'{company_name}/locations.html', states_url),
        'clinics': (f'{company_name}/tn.html', f'{states_url}?state=tn#top'),
    })