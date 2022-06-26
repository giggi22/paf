import argparse
from . import functions as fc


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


if __name__ == '__main__':
    main()
