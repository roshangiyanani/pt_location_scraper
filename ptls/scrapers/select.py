from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class Select:
    company_name = 'Select'
    company_name_upper = company_name.upper()

    base_url: str = 'https://www.selectphysicaltherapy.com'

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'communities': (f'{company_name}/communities.html', 'https://www.selectphysicaltherapy.com/about/your-local-community/'),
        'locations': (f'{company_name}/locations.html','https://www.selectphysicaltherapy.com/community/alaska/'),
    })

    images: Dict[str, str] = {
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos/OP_Select-Physical-Therapy---USE-THIS-ONE-ON-THE-SCROLL.png?n=6636': 'Select Physical Therapy',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos_v2/Banner-PT-logo.png': 'Banner Physical Therapy',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos/OP_NovaCare.png?n=8181': 'NovaCare Rehabilitation',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos/EmoryLogo.jpg': 'Emory Rehabilitation Outpatient Center',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos/Physio-Logo_MR-Small.png': 'Phsyio',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos_v2/OP_SelectKids-logo.png': 'Select Kids Pediatric Therapy',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos_v2/UHM-Select-PT-logo.png': 'UnityPoint Health Marshalltown',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos_v2/OP_NovaCareKids-logo.png':
        'NovaCare Kids Pediatric Therapy',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos/MichianaOrthoSportLogo.png':
        'Michiana Orthopaedic & Sports Physical Therapy',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos_v2/LBH-PT-logo.png?n=2572': 'Lifebridge Health',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos/OP_wellspan-logo.png':
        'NovaCare Rehabilitiation in collaboration with Wellspan Ephrats Community Hospital',
        '/uploadedImages/NovaCareSelectPT/Content/Shared/Brand_Logos_v2/PSH-Rehab-logo.png':
        'PennState Health Rehabilition Hospital',
    }

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')
        total_location_count: int = 0

        communities: [str] = cls._get_communities(req.get_page_bs(cls.test_urls['communities'][1]))
        communities_len: int = len(communities)
        communities_count: int = 0
        for communities_url in communities:
            communities_count = communities_count + 1
            sys.stdout.write(f'\r{cls.company_name_upper}: Processing community {communities_count}/{communities_len}.')

            locations: [Clinic] = cls._get_clinics(req.get_page_bs(communities_url))
            total_location_count = total_location_count + len(locations)
            for clinic in locations:
                yield clinic

        sys.stdout.write(f'\r{cls.company_name_upper}: Processed {communities_len} communities to find {total_location_count} clinics.\n')

    @classmethod
    def _get_communities(cls, page: BeautifulSoup) -> [str]:
        urls: [str] = list()
        for link in page.find('div', {'class': 'communities'}).find_all('a'):
            link_address: str = link.get('href')
            url: str = f'{cls.base_url}{link_address}'
            urls.append(url)
        return urls

    @classmethod
    def _get_clinics(cls, page: BeautifulSoup) -> [Clinic]:
        locations: [Clinic] = list()
        for box in page.find('div', {'class': 'results'}).find_all('div', {'class': 'row'}):
            name: str = box.find('span', {'class': 'name'}).string.strip()
            address: Address = Address.from_address_str(' '.join(box.find('div', {'class': 'address'}).stripped_strings))
            numbers = box.find_all('span', {'class': 'phone'})
            phone: str = (numbers[0].string or '').strip()
            fax: str = (numbers[1].string or '').strip()[:14]
            company: str = cls.images[box.find('div', {'class': 'logo'}).find('img').get('src')]
            url_part: str = box.find('a', {'class': 'button-website'}).get('href')
            url: str = f'{cls.base_url}{url_part}'
            clinic: Clinic = Clinic(company, name, address, phone, url, fax=fax)
            locations.append(clinic)
        return locations