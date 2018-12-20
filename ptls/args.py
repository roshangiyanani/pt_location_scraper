import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--location', action='store', help='directory to store the files in')
parser.add_argument('-d', '--delay', action='store', help='delay for network requests (in seconds)', type=float)

class Args:

    out_location: Path
    network_delay: float

    def __init__(self):
        self._set_location('./data')
        self._set_network_delay(0.1)

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

def get_args() -> Args:
    pargs = parser.parse_args()
    args = Args()

    if pargs.location:
        args._set_location(pargs.location)

    if pargs.delay:
        args._set_network_delay(pargs.delay)

    return args