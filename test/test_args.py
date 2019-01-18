import unittest

from ptls.args import Args, get_args
from ptls.scrapers import SCRAPERS, ATI, Pivot
from pathlib import Path

class TestArgsClass(unittest.TestCase):

    def test_constructor(self):
        args: Args = Args()

    def test_set_location(self):
        args: Args = Args('./data')
        self.assertEqual(args.out_location, Path('./data'))
        args._set_location('./build')
        self.assertEqual(args.out_location, Path('./build'))

        # Should fail on file or nonexistent directory
        with self.assertRaises(NotADirectoryError):
            args._set_location('test/test_args.py')
        with self.assertRaises(FileNotFoundError):
            args._set_location('abcdefg')
    
    def test_all_scrapers(self):
        args: Args = get_args(['--all-scrapers'], '/dev')
        for scraper in SCRAPERS.values():
            self.assertIn(scraper, args.scrapers)

    def test_some_scrapers(self):
        args: Args = get_args(['--scrapers', ATI.company_name, Pivot.company_name], '/dev')

        self.assertIn(ATI, args.scrapers)
        self.assertIn(Pivot, args.scrapers)

        for scraper in SCRAPERS.values():
            if scraper != ATI and scraper != Pivot:
                self.assertNotIn(scraper, args.scrapers)