import csv
from pathlib import Path


class Clinic:
    company: str
    name: str
    address: str
    phone: str or None
    fax: str or None
    email: str or None
    url: str or None

    def __init__(self, company: str, name: str, address: str, phone: str or None = None,
                 url: str or None = None, fax: str or None = None, email: str or None = None):
        self.company = company
        self.name = name
        self.address = address
        self.phone = phone
        self.url = url
        self.fax = fax
        self.email = email

    def as_row(self) -> [str]:
        return [self.company or '', self.name or '', self.address or '',
                self.url or '', self.phone or '', self.email or '', self.fax or '']

    @staticmethod
    def get_header() -> [str]:
        return ['company', 'name', 'address', 'url', 'phone', 'email', 'fax']

    def __eq__(self, other):
        return self.company == other.company \
               and self.name == other.name \
               and self.address == other.address \
               and self.phone == other.phone \
               and self.url == other.url \
               and self.fax == other.fax \
               and self.email == other.email

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


def write_clinic_list(clinics: [Clinic], file: Path):
    with file.with_suffix('.csv').open('w', newline='') as csvfile:
        writer = csv.writer(csvfile, 'excel')
        writer.writerow(Clinic.get_header())
        for clinic in clinics:
            writer.writerow(clinic.as_row())
