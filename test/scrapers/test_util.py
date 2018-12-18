import unittest

from ptls.scrapers.util import get_page

class TestScraperUtilClass(unittest.TestCase):

    def test_valid(self):
        self.assertIsNotNone(get_page('https://www.google.com'))

    # def test_invalid(self):
    #     self.assertIsNone(get_page('google.com'))