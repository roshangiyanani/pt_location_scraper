import usaddress
from uszipcode import SearchEngine, SimpleZipcode

search: SearchEngine = SearchEngine()

def parse_zip(address_str: str) -> str:
    address = usaddress.parse(address_str)
    for (value, component) in address:
        if component == 'ZipCode':
            return value
    return None

def get_zip(city: str, state: str) -> str:
    zipcodes: [SimpleZipcode] = search.by_city_and_state(city, state)
    if len(zipcodes) == 1:
        return zipcodes[0].zipcode
    else:
        return None