import argparse
from . import functions as fc

# TODO per testing controllare che le costanti vengano create/lette/eliminate correttamente

def main():
    # parser initialization
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='possible actions', dest='subparser')

    # PLOT argument
    plot_parser = subparsers.add_parser('plot', help='plot the data')
    plot_parser.add_argument("path", help='path to data to plot', type=str, nargs=1)
    plot_parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    # FIT argument
    fit_parser = subparsers.add_parser('fit', help='fit the data')

    # CONSTANTS argument
    constants_parser = subparsers.add_parser('const', help='manage the constants')
    constants_parser.add_argument("-a", "--add", help="add a new constant", action="store_true")
    constants_parser.add_argument("-d", "--delete", help="delete a constant", action="store_true")

    # arguments are converted into an argparser.Namespace object
    args = parser.parse_args()

    # MAIN IF STATEMENTS
    # plot case
    if args.subparser == 'plot':
        path = args.path[0] if isinstance(args.path, list) else args.path
        if args.verbose:
            fc.plot_data_verbose()
        else:
            data = fc.read_data(path)
            fc.plot_data(data)

    # fit case
    if args.subparser == 'fit':
        fc.fitting_procedure()

    # const case
    if args.subparser == 'const':
        fc.initialize_constants()
        if args.add:
            fc.add_constant()
        if args.delete:
            fc.delete_constant()
        fc.print_constants()


if __name__ == '__main__':
    main()
