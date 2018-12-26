import unittest

from ptls.address import parse_zip

class TestAddressClass(unittest.TestCase):

    def test_parse_zip(self):
        address: str = '21043 N. Cave Creek Rd., Ste. A1 Phoenix, AZ 85024'
        self.assertEqual('85024', parse_zip(address))
        address = '21043 N. Cave Creek Rd., Ste. A1 85024'
        self.assertEqual('85024', parse_zip(address))
