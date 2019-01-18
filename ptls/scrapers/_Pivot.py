from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class Pivot:

    base_url: str = 'https://www.pivotphysicaltherapy.com'

    company_name = 'Pivot'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'states': (f'states.html', f'{base_url}/locations/'),
        'locations': (f'wv.html', f'{base_url}/locations/search-west-virginia/'),
        'clinic': (f'inwood.html', f'{base_url}/locations/inwood/'),
    })

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')
        total_location_count: int = 0

        states: [str] = cls._get_states(req.get_page_bs(cls.test_urls['states'][1]))
        states_len: int = len(states)
        state_count: int = 0
        for state in states:
            state_count = state_count + 1
            sys.stdout.write(f'\r{cls.company_name_upper}: Processing state {state_count}/{states_len}.')

            locations: [str] = cls._get_locations(req.form_json('post', f'{cls.base_url}/wp-admin/admin-ajax.php?', data={
                'action': 'markersearch',
                'method': 'state',
                'state': state,
            }))

            locations_len: int = len(locations)
            total_location_count = total_location_count + locations_len
            location_count: int = 0
            for location_url in locations:
                location_count = location_count + 1
                sys.stdout.write(f'\r{cls.company_name_upper}: Processing state {state_count}/{states_len} and location {location_count}/{locations_len}.')

                clinic: Clinic = cls._get_profile(req.get_page_bs(location_url), location_url)
                yield clinic
        
        sys.stdout.write(f'\r{cls.company_name_upper}: Processed {states_len} states to find {total_location_count} clinics.\n')


    @classmethod
    def _get_states(cls, page: BeautifulSoup) -> [str]:
        states: [str] = list()
        for link in page.find_all('div', {'class': 'locations-list-container'})[1].find_all('a'):
            state: str = link.get('data-state')
            states.append(state)
        return states


    @classmethod
    def _get_locations(cls, resp) -> [str]:
        urls: [str] = list()
        for location in resp['markers']:
            html: BeautifulSoup = BeautifulSoup(location['list_format'], features='lxml')
            url: str = html.find('a').get('href')
            urls.append(url)
        return urls


    @classmethod
    def _get_profile(cls, page: BeautifulSoup, url: str) -> Clinic:
        name: str = page.find('h2', {'class': 'location-name'}).stripped_strings.__next__().strip()
        address: Address = Address.from_address_str(' '.join(page.find('address').stripped_strings))
        numbers = page.find('div', {'class': 'location-phone'}).contents
        phone: str = numbers[0].strip()[6:]
        fax: str = numbers[2].strip()[4:]
        try:
            email: str = page.find('div', {'class': 'location-email'}).contents[0].strip()
        except:
            email: str = None
        clinic: Clinic = Clinic(cls.company_name, name, address, phone, url, fax=fax, email=email)
        return clinic
