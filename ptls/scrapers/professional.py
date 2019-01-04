from typing import Dict, Tuple

class Professional:
    company_name = 'Professional Physical Therapy'
    company_name_upper = company_name.upper()

    base_url: str = 'https://www.professionalpt.com'

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'communities': ('communities.html', f'{base_url}/physical-therapy-clinics/'),
        'profile': ('broad_street.html', f'{base_url}/office/broad-street/'),
    })