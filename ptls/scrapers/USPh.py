from typing import Dict, Tuple

states_url: str = 'http://usph.com/corporate/clinic-locations.aspx'

test_urls: Dict[str, Tuple[str, str]] = dict({
    'states': ('usph/locations.html', states_url),
    'clinics': ('usph/tn.html', f'{states_url}?state=tn#top'),
})