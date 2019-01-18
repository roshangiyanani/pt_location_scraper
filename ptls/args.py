import argparse
from pathlib import Path
from typing import Set
from ptls.scrapers import SCRAPERS, Athletico, ATI, CORA, Pivot, Professional, Select, URPT, USPh

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--location', action='store', help='directory to store the files in (defaults to ./data/)')
parser.add_argument('-d', '--delay', action='store', help='delay for network requests in seconds (defaults to 0.1)', type=float)

clinic_or_all_group = parser.add_mutually_exclusive_group(required=True)
clinic_or_all_group.add_argument('-a', '--all-scrapers', action='store_true', help='run for all clinics')
clinic_or_all_group.add_argument('--scrapers', nargs='+', choices=SCRAPERS, help='run for selected clinic(s)')

class Args:

    def __init__(self, default_location: str = './data'):
        self._set_location(default_location)
        self._set_network_delay(0.1)
        self.scrapers = set()

    def _set_location(self, location: str):
        p: Path = Path(location)
        if not p.exists():
            raise FileNotFoundError(f'{str(p)} does not exist')
        if not p.is_dir():
            raise NotADirectoryError(f'{str(p)} is not a directory')
        self.out_location = p

    def _set_network_delay(self, delay: float):
        if delay < 0:
            raise FloatingPointError(f'delay ({delay}) must be >= 0 seconds')
        self.network_delay = delay

    def _add_scapers(self, scrapers: [str]):
        for scraper in scrapers:
            self.scrapers.add(SCRAPERS[scraper])
    
    def _add_all_scrapers(self):
        for scraper in SCRAPERS.values():
            self.scrapers.add(scraper)

def get_args(args_in: [str] or None = None, default_location: str = './data') -> Args:
    if args_in is None:
        pargs = parser.parse_args()
    else:
        pargs = parser.parse_args(args_in)
    
    args = Args(default_location)

    if pargs.location:
        args._set_location(pargs.location)

    if pargs.delay:
        args._set_network_delay(pargs.delay)
    
    if pargs.all_scrapers:
        args._add_all_scrapers()
    else:
        args._add_scapers(pargs.scrapers)

    return args