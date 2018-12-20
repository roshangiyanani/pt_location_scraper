from args import Args, get_args
from clinic import Clinic, write_clinic_list
from scrapers.athletico import Athletico
from scrapers.ATI import ATI
from requester import Requester

args: Args = get_args()
print(f'Output location is "{str(args.out_location.resolve())}/".')
print(f'Network delay is {args.network_delay} seconds.')

req: Requester = Requester(args.network_delay)

clinics = [
    (Athletico, 'athletico'),
    (ATI, 'ati')
]

for (company_scraper, company) in clinics:
    write_clinic_list(company_scraper.run(req), args.out_location.joinpath(company))