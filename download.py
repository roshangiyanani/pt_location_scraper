from ptls.scrapers.athletico import states_location_url
from ptls.scrapers.util import get_page

print('Downloading athletico test files...')
with open('./test/scrapers/test_files/athletico/locations.html', 'wb') as text_file:
    raw_html: str = get_page(states_location_url)
    text_file.write(raw_html)

with open('./test/scrapers/test_files/athletico/illinois.html', 'wb') as text_file:
    raw_html: str = get_page('http://www.athletico.com/regions/illinois/')
    text_file.write(raw_html)