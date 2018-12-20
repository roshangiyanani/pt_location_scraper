from typing import Dict, Tuple

states_url: str = 'https://locations.atipt.com'

test_urls: Dict[str, Tuple[str, str]] = dict({
    'states': ('ati/locations.html', states_url),
    'locations': ('ati/ma.html', 'https://locations.atipt.com/ma'),
    'clinics': ('ati/fairbanks.html', 'https://locations.atipt.com/ak/fairbanks'),
    'profile': ('ati/fairbanks-ak.html', 'https://locations.atipt.com/fairbanks-ak'),
})