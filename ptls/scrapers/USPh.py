from typing import Dict, Tuple

states_url: str = 'http://usph.com/corporate/clinic-locations.aspx'

class USPh:
    company_name = 'USPh'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'states': (f'{company_name}/locations.html', states_url),
        'clinics': (f'{company_name}/tn.html', f'{states_url}?state=tn#top'),
    })