from ptls.requester import Requester
from ptls.scrapers.athletico import Athletico
from ptls.scrapers.ATI import ATI
from ptls.scrapers.pivot import Pivot
from ptls.scrapers.professional import Professional
from ptls.scrapers.select import Select
from ptls.scrapers.USPh import USPh
from pathlib import Path

req: Requester = Requester(0.2)
path: Path = Path('./data/test_files')

def download(file: Path, url: str):
    file.open('wb').write(req.get_page_str(url))

clinic_scrapers = [
    Athletico,
    ATI,
    Pivot,
    Professional,
    Select,
    USPh,
]

for scraper in clinic_scrapers:
    print(f'Downloading {scraper.company_name} test files...')
    
    scraper_path: Path = path.joinpath(scraper.company_name)
    scraper_path.mkdir(parents=True, exist_ok=True)

    for (p, url) in scraper.test_urls.values():
        download(scraper_path.joinpath(p), url)