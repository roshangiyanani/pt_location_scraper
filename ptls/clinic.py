
class Clinic:
    company: str
    name: str
    address: str
    phone: str
    fax: str
    email: str
    url: str

    def __init__(self, company: str, name: str, address: str, phone: str, url: str, fax: str = None, email: str = None):
        self.company = company
        self.name = name
        self.address = address
        self.phone = phone
        self.url = url
        self.fax = fax
        self.email = email

    def __eq__(self, other):
        return self.company == other.company\
            and self.name == other.name\
            and self.address == other.address\
            and self.phone == other.phone\
            and self.url == other.url\
            and self.fax == other.fax\
            and self.email == other.email\

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '\n'.join([
            f'company: {self.company}',
            f'location_name: {self.name}',
            f'address: {self.address}',
            f'phone: {self.phone}',
            f'url: {self.url}',
            f'fax: {self.fax}',
            f'email: {self.email}',
        ])