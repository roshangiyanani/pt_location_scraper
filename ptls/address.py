import usaddress

def parse_zip(address_str: str) -> str:
    address = usaddress.parse(address_str)
    for (value, component) in address:
        if component == 'ZipCode':
            return value