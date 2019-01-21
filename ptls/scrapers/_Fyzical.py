from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class Fyzical:

    base_url: str = 'https://www.fyzical.com'

    company_name = 'Fyzical'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'locations': (f'locations.html', f'{base_url}/locations.php'),
        'multiple': (f'flint_river.html', f'{base_url}/flint-river'),
        'single': (f'west_princeton.html', f'{base_url}/west-princeton'),
        'one_of': (f'camilla.html', f'{base_url}/flint-river/FYZICAL-Camilla'),
    })

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')
        total_location_count: int = 0

        resp = req.form_json('post', 'https://manage.fyzical.com/locationsearch', data={
                'lng': -100,
                'lat': 40,
                'radius': 5000,
            })
        locations = resp['data']

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
        name: str = loc['name'][8:]
        address: Address = Address(None, loc['address'], None, loc['city'], loc['state'], loc['zip'])
        phone: str = loc['phone']
        fax: str = loc['fax']
        email: str = loc['email']
        url: str = f'{cls.base_url}/{loc["slug"]}'
        return Clinic(cls.company_name, name, address, phone, url, fax=fax, email=email)