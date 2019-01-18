from bs4 import BeautifulSoup
import sys
from typing import Dict, Iterator, List, Tuple

from ptls.address import Address
from ptls.clinic import Clinic
from ptls.requester import Requester

class Professional:
    company_name = 'Professional'
    company_name_upper = company_name.upper()

    base_url: str = 'https://www.professionalpt.com'

    test_urls: Dict[str, Tuple[str, str]] = dict({
        'communities': ('communities.html', f'{base_url}/physical-therapy-clinics/'),
        'profile': ('broad_street.html', f'{base_url}/office/broad-street/'),
    })

    @classmethod
    def run(cls, req: Requester) -> Iterator[Clinic]:
        sys.stdout.write(f'\r{cls.company_name_upper}: Processing.')
        total_location_count: int = 0

        communities: [[str]] = cls._get_communities(req.get_page_bs(cls.test_urls['communities'][1]))
        communities_len: int = len(communities)
        communities_count: int = 0
        for community_urls in communities:
            communities_count = communities_count + 1
            sys.stdout.write(f'\r{cls.company_name_upper}: Processing community {communities_count}/{communities_len}.')

            locations_len: int = len(community_urls)
            location_count: int = 0
            for url in community_urls:
                location_count = location_count + 1
                sys.stdout.write(
                    f'\r{cls.company_name_upper}: Processing community {communities_count}/{communities_len} and location {location_count}/{locations_len}.')
                yield cls._get_clinic(req.get_page_bs(url), url)
            total_location_count = total_location_count + locations_len

        sys.stdout.write(f'\r{cls.company_name_upper}: Processed {communities_len} communities to find {total_location_count} clinics.\n')

    @classmethod
    def _get_communities(cls, page: BeautifulSoup) -> List[List[str]]:
        communities: [str] = list()
        for group in page.find_all('div', {'class': 'accordion-group'}):
            urls: [str] = list()
            for inner_grp in group.find_all('div', {'class': 'accordion-inner'}):
                for link in inner_grp.find_all('a'):
                    link_address: str = link.get('href')
                    urls.append(link_address)
            communities.append(urls)
        return communities
    
    @classmethod
    def _get_clinic(cls, page: BeautifulSoup, url: str) -> [Clinic]:
        name: str = page.find('h1', {'class': 'entry-title'}).string.strip()
        info = page.find('div', {'class': 'card'}).find_all('p')
        for p in info:
            try:
                address: Address = Address.from_address_str(' '.join(p.stripped_strings))
                break
            except:
                continue
        phone: str or None = None
        fax: str or None = None
        for p in info:
            links = p.find_all('a')
            if len(links) == 2:
                phone = links[0].string.strip()
                fax = links[1].string.strip()
                break
        clinic: Clinic = Clinic(cls.company_name, name, address, phone, url, fax=fax)
        return clinic
