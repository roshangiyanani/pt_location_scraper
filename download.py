from pathlib import Path

from ptls.requester import Requester
from ptls.args import Args, get_args

args: Args = get_args(default_location='./data/test_files')
req: Requester = Requester(args.network_delay)

def download(file: Path, url: str):
    file.open('wb').write(req.get_page_str(url))

for scraper in args.scrapers:
    print(f'Downloading {scraper.company_name} test files...')
    
    scraper_path: Path = args.out_location.joinpath(scraper.company_name)
    scraper_path.mkdir(parents=True, exist_ok=True)

    for (p, url) in scraper.test_urls.values():
        download(scraper_path.joinpath(p), url)