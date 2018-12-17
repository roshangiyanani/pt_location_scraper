import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--location', action='store', help='directory to store the files in')

class Args:

    out_location: Path

    def __init__(self):
        self.set_location('./data')

    def set_location(self, location: str):
        p: Path = Path(location)
        if not p.exists():
            raise FileNotFoundError(f'{str(p)} does not exist')
        if not p.is_dir():
            raise NotADirectoryError(f'{str(p)} is not a directory')
        self.out_location = p

def get_args() -> Args:
    pargs = parser.parse_args()
    args = Args()

    if pargs.location:
        args.set_location(pargs.location)

    return args