from ptls.requester import Requester
from ptls.scrapers.athletico import Athletico
from ptls.scrapers.ATI import ATI
from ptls.scrapers.USPh import USPh
from ptls.scrapers.select import Select
from pathlib import Path

req: Requester = Requester(0.2)
path: Path = Path('./data/test_files')

def download(file: Path, url: str):
    file.open('wb').write(req.get_page_str(url))

clinic_scrapers = [
    Athletico,
    ATI,
    USPh,
    Select,
]

for scraper in clinic_scrapers:
    print(f'Downloading {scraper.company_name} test files...')
    for (p, url) in scraper.test_urls.values():
        download(path.joinpath(p), url)