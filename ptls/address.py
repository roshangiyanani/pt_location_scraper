import usaddress
from scourgify import normalize_address_record
from uszipcode import SearchEngine, SimpleZipcode

search: SearchEngine = SearchEngine()

def get_zip(city: str, state: str) -> str:
    zipcodes: [SimpleZipcode] = search.by_city_and_state(city, state)
    if len(zipcodes) == 1:
        return zipcodes[0].zipcode
    else:
        return None

class Address:
    raw: str
    address_line_1: str or None
    address_line_2: str or None
    city: str
    state: str
    zipcode: str or None
    
    def __init__(self, raw: str or None, address_line_1: str or None, address_line_2: str or None,
                 city: str, state: str, zipcode: str or None):
        self.raw = raw
        if self.raw is None:
            self.raw = f'{address_line_1} {address_line_2}, {city}, {state} {zipcode}'
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def __eq__(self, other) -> bool:
        return self.address_line_1 == other.address_line_1 \
            and self.address_line_2 == other.address_line_2 \
            and self.city == other.city \
            and self.state == other.state \
            and self.zipcode == other.zipcode

    def __str__(self) -> str:
        return self.raw
    
    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_address_str(cls, address_str: str):
        try:
            address_dict = normalize_address_record(address_str)
            return Address(address_str, address_dict['address_line_1'],
                       address_dict['address_line_2'], address_dict['city'], 
                       address_dict['state'], address_dict['postal_code'])
        except:
            address = usaddress.parse(address_str)
            address_dict = dict()
            for (part, tag) in address:
                address_dict[tag] = part
            return Address(address_str, None, None, address_dict['PlaceName'],
                           address_dict['StateName'], address_dict['ZipCode'])
    
    @classmethod
    def from_city_state(cls, city: str, state: str):
        zip: str or None = get_zip(city, state)
        return Address(f'{city}, {state}', None, None, city, state, zip)