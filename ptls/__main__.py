from args import Args, get_args
from clinic import Clinic, write_clinic_list
from scrapers.athletico import Athletico
from scrapers.ATI import ATI
from scrapers.cora import CORA
from scrapers.pivot import Pivot
from scrapers.professional import Professional
from scrapers.select import Select
from scrapers.URPT import URPT
from scrapers.USPh import USPh
from requester import Requester

args: Args = get_args()
print(f'Output location is "{str(args.out_location.resolve())}/".')
print(f'Network delay is {args.network_delay} seconds.')

req: Requester = Requester(args.network_delay)

clinic_scrapers = [
    Athletico,
    ATI,
    CORA,
    Pivot,
    Professional,
    Select,
    URPT,
    USPh,
]

for scraper in clinic_scrapers:
    write_clinic_list(scraper.run(req), args.out_location.joinpath(scraper.company_name))