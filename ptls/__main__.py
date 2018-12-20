from args import Args, get_args
from clinic import Clinic, write_clinic_list
from scrapers.athletico import Athletico
from scrapers.ATI import ATI
from requester import Requester

args: Args = get_args()
print(f'Output location is "{str(args.out_location)}/".')
print(f'Network delay is {args.network_delay} seconds.')

req: Requester = Requester(args.network_delay)
write_clinic_list(Athletico.run(req), args.out_location.joinpath('athletico'))
write_clinic_list(ATI.run(req), args.out_location.joinpath('ati'))