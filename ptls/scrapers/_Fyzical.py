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