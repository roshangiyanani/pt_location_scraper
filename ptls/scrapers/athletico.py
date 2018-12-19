from ptls.scrapers.util import get_page
from ptls.clinic import Clinic
from bs4 import BeautifulSoup
import re
from re import Match

base_url: str = 'https://www.athletico.com'
states_location_url: str = f'{base_url}/locations/'

regionMatch = re.compile('/region/*')

def get_states_location_urls(raw_html: str) -> [str]:
    page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    urls: [str] = list()
    for link in page.find(id='awardsTiles').find_all('a'):
        # print(link)
        link_address: str = link.get('href')
        if regionMatch.match(link_address) is not None:
            urls.append(f'{base_url}{link_address}')
    return urls

locationMatch = re.compile('/locations/*')

def get_state_location_urls(raw_html: str) -> [str]:
    page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    urls: [str] = list()
    for link in page.find('div', { 'class': 'pf-content'}).find_all('a'):
        link_address: str = link.get('href')
        if locationMatch.match(link_address) is not None:
            urls.append(f'{base_url}{link_address}')
    return urls

phoneMatch = re.compile('(tel:)(.*)')
emailMatch = re.compile('(mailto:)(.*)')

def get_location_info(raw_html: str, url: str) -> Clinic:
    page: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    company: str = 'Athletico Physical Therapy'
    location_name: str = page.find('h1', { 'class': 'innerPage' }).string
    address: str = ' '.join(page.find('div', id='geographicInfo')\
        .find('p', { 'class': 'subheadText'}).stripped_strings)
    phone = None
    email = None
    for link in page.find('div', id='contactInfo').find_all('a'):
        link_address: str | None = link.get('href')
        if link_address is not None:
            phone_match: Match = phoneMatch.match(link_address)
            email_match: Match = emailMatch.match(link_address)
            if phone_match is not None:
                phone: str = phone_match[2].strip()
            elif email_match is not None:
                email: str = email_match[2].strip()
    fax: str = page.find('div', id='contactInfo').find('div').find('span').string
    return Clinic(company, location_name, address, phone, url, fax, email)