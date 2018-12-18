from ptls.scrapers.util import get_page
from bs4 import BeautifulSoup
import re

base_url: str = 'https://www.athletico.com'
states_location_url: str = f'{base_url}/locations/'

def get_states_location_urls(raw_html: str) -> [str]:
    page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    urls: [str] = list()
    regionMatch = re.compile('/region/*')
    for link in page.find(id='awardsTiles').find_all('a'):
        # print(link)
        link_address: str = link.get('href')
        if regionMatch.match(link_address) is not None:
            urls.append(f'{base_url}{link_address}')
    return urls

def get_state_location_urls(raw_html: str) -> [str]:
    page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    urls: [str] = list()
    locationMatch = re.compile('/locations/*')
    for link in page.find('div', { 'class': 'pf-content'}).find_all('a'):
        link_address: str = link.get('href')
        if locationMatch.match(link_address) is not None:
            urls.append(f'{base_url}{link_address}')
