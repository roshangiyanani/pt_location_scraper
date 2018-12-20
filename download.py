from ptls.requester import Requester
from ptls.scrapers.athletico import test_urls as athletico_test_urls
from ptls.scrapers.ATI import test_urls as ati_test_urls
from pathlib import Path

req: Requester = Requester(0.2)
path: Path = Path('./data/test_files')

def download(file: Path, url: str):
    file.open('wb').write(req.get_page_str(url))


print('Downloading athletico test files...')
for (p, url) in athletico_test_urls.values():
    download(path.joinpath(p), url)

print('Downloading ATI test files...')
for (p, url) in ati_test_urls.values():
    download(path.joinpath(p), url)