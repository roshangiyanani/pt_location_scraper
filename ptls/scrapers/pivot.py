from typing import Dict, Tuple

class Pivot:

    base_url: str = 'https://www.pivotphysicaltherapy.com'

    company_name = 'Pivot Physical Therapy'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'states': (f'states.html', f'{base_url}/locations/'),
        'locations': (f'wv.html', f'{base_url}/locations/search-west-virginia/'),
        'clinic': (f'inwood.html', f'{base_url}/locations/inwood/'),
    })