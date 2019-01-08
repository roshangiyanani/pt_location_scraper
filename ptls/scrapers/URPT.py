from bs4 import BeautifulSoup
import json
import sys
from typing import Dict, Iterator, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class URPT:
    base_url: str = 'https://urpt.com/locations'

    company_name = 'URPT'
    company_name_upper = company_name.upper()

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')

        data = cls._get_data(req.get_page_bs(cls.base_url))
        data_len: int = len(data)
        data_count: int = 0
        for d in data:
            data_count = data_count + 1
            sys.stdout.write(f'\r{cls.company_name_upper}: Processing location {data_count}/{data_len}.')
            yield cls._get_clinic(d)
        sys.stdout.write(f'\r{cls.company_name_upper}: Processed {data_len} clinics.\n')

    @classmethod
    def _get_data(cls, page: BeautifulSoup):
        # extract json/data structure
        script = page.find('div', {'class': 'location-list'}).script.string.split('\n')
        data_str = [x.strip() for x in script if x.lstrip().startswith('var locations = ')][0]

        # convert to python object
        array_str = data_str[16:-3]
        array_str += ']'
        data = json.loads(array_str)
        return data

    @classmethod
    def _get_clinic(cls, d: Dict):
        company = d['brand']
        name = d['name'][0]
        address = Address.from_address_str(' '.join([d['address'], d['city'], d['state'], d['zip']]))
        phone = d['phone']
        url = d['href']
        fax = d['fax']
        return Clinic(company, name, address, phone, url, fax=fax)


    test_urls: Dict[str, Tuple[str, str]] = dict({
        'all': (f'all.html', base_url),
    })