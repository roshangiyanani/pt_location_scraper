import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

class Args:

    out_location: Path

    def __init__(self):
        self.set_location('./data')

    def set_location(self, location: str):
        p: Path = Path(location)
        self.out_location = p