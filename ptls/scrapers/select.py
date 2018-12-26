from typing import Dict, Tuple

class Select:
    company_name = 'Select'
    company_name_upper = company_name.upper()

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'communities': (f'{company_name}/communities.html', 'https://www.selectphysicaltherapy.com/about/your-local-community/'),
        'locations': (f'{company_name}/locations.html','https://www.selectphysicaltherapy.com/community/alaska/'),
    })