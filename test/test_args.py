import unittest

from ptls.args import Args
from pathlib import Path

class TestArgsClass(unittest.TestCase):

    def test_constructor(self):
        args: Args = Args()

    def test_set_location(self):
        args: Args = Args()
        self.assertEqual(args.out_location, Path('./data'))
        args._set_location('./build')
        self.assertEqual(args.out_location, Path('./build'))

        # Should fail on file or nonexistent directory
        with self.assertRaises(NotADirectoryError):
            args._set_location('test/test_args.py')
        with self.assertRaises(FileNotFoundError):
            args._set_location('abcdefg')