import unittest

from ptls.address import Address, get_zip

class TestAddressClass(unittest.TestCase):

    def test_from_address_str(self):
        address: str = '21043 N. Cave Creek Rd., Ste. A1 Phoenix, AZ 85024'
        self.assertEqual(Address.from_address_str(address).zipcode, '85024')

    def test_from_city_state(self):
        city: str = 'Voorhees'
        state: str = 'NJ'
        address: Address = Address.from_city_state(city, state)
        self.assertEqual(address.city, city)
        self.assertEqual(address.state, state)
        self.assertEqual(address.zipcode, '08043')

    def test_get_zip(self):
        city: str = 'Voorhees'
        state: str = 'NJ'
        self.assertEqual('08043', get_zip(city, state))

        city = 'Bethlehem'
        state = 'PA'
        self.assertEqual('18015', get_zip(city, state))
