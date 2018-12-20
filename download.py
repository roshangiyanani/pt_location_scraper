from ptls.requester import Requester

req: Requester = Requester(0.2)

print('Downloading athletico test files...')
with open('./test/scrapers/test_files/athletico/locations.html', 'wb') as text_file:
    raw_html: str = req.get_page_str('http://www.athletico.com/locations/')
    text_file.write(raw_html)

with open('./test/scrapers/test_files/athletico/illinois.html', 'wb') as text_file:
    raw_html: str = req.get_page_str('http://www.athletico.com/regions/illinois/')
    text_file.write(raw_html)

with open('./test/scrapers/test_files/athletico/bloomington.html', 'wb') as text_file:
    raw_html: str = req.get_page_str('http://www.athletico.com/locations/bloomington-illinois/?location=bloomington-illinois')
    text_file.write(raw_html)