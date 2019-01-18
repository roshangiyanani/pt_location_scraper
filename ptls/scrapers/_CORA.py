from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class CORA:

    base_url: str = 'https://www.coraphysicaltherapy.com'

    company_name = 'CORA'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'all': (f'locations.html', f'{base_url}/locations/'),
        'profile': (f'batesburg-sc.html', f'{base_url}/batesburg-south-carolina/'),
    })

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')
        total_location_count: int = 0

        locations = req.form_json('get', f'{cls.base_url}/wp-admin/admin-ajax.php?', params={
                'action': 'store_search',
                'lat': 30,
                'long': -80,
                'max_results': 25,
                'search_radius': 50,
                'autoload': 1,
            })

        locations_len: int = len(locations)
        total_location_count = total_location_count + locations_len
        location_count: int = 0
        for location in locations:
            sys.stdout.write(f'\r{cls.company_name_upper}: Processing location {location_count}/{locations_len}.')

            clinic: Clinic = cls._get_profile(location)
            yield clinic
        
        sys.stdout.write(f'\r{cls.company_name_upper}: Processed {total_location_count} clinics.\n')
    
    @classmethod
    def _get_profile(cls, loc):
        name: str = loc['store'][5:]
        address: Address = Address(None, loc['address'], None, loc['city'], loc['state'], loc['zip'])
        phone: str = loc['phone']
        fax: str = loc['fax']
        email: str = loc['email']
        url: str = f'{cls.base_url}{loc["url"]}'
        return Clinic(cls.company_name, name, address, phone, url, fax=fax, email=email)