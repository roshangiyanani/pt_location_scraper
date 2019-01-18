from args import Args, get_args
from clinic import Clinic, write_clinic_list
from requester import Requester

args: Args = get_args()
print(f'Output location is "{str(args.out_location.resolve())}/".')
print(f'Network delay is {args.network_delay} seconds.')

req: Requester = Requester(args.network_delay)

for scraper in args.scrapers:
    write_clinic_list(scraper.run(req), args.out_location.joinpath(scraper.company_name))