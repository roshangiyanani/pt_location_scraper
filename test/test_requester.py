import unittest

from ptls.requester import Requester

class TestRequesterClass(unittest.TestCase):
    _req: Requester

    def setUp(self):
        self._req = Requester(0.2)

    def test_valid(self):
        self.assertIsNotNone(self._req.get_page_str('https://www.google.com'))
        self.assertIsNotNone(self._req.get_page_bs('https://www.google.com'))