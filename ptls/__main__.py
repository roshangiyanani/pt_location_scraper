from ptls.args import Args, get_args

args: Args = get_args()
print(f"Output location is '{str(args.out_location)}/'");