from ptls.requester import Requester
from ptls.scrapers.athletico import test_urls as athletico_test_urls
from ptls.scrapers.ATI import test_urls as ati_test_urls
from ptls.scrapers.USPh import test_urls as usph_test_urls
from pathlib import Path

req: Requester = Requester(0.2)
path: Path = Path('./data/test_files')

def download(file: Path, url: str):
    file.open('wb').write(req.get_page_str(url))

test_urls_pairs = [
    (athletico_test_urls, 'athletico'),
    (ati_test_urls, 'ati'),
    (usph_test_urls, 'usph'),
]

for (test_urls, name) in test_urls_pairs:
    print(f'Downloading {name} test files...')
    for (p, url) in test_urls.values():
        download(path.joinpath(p), url)