import unittest

from ptls.args import Args
from pathlib import Path

class TestArgsClass(unittest.TestCase):

    def test_constructor(self):
        args: Args = Args()

    def test_set_location(self):
        args: Args = Args()
        self.assertEqual(args.out_location, Path('./data'))
        args.set_location('./build')
        self.assertEqual(args.out_location, Path('./build'))