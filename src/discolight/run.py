import argparse
import sys

from .augmentor import Augmentor
from .query import load_query


def run(augmentor, command):

    if command == "generate":
        augmentor.generate()
    else:
        raise NameError("No such command {}".format(command))


def main(args=None):
    parser = argparse.ArgumentParser(description="Augmentor")

    parser.add_argument("command",
                        metavar="COMMAND",
                        help="The command to run")
    parser.add_argument("query_file",
                        metavar="QUERY_FILE",
                        nargs='?',
                        default=None,
                        help="The file to load the query from")

    args = parser.parse_args(args)

    if args.query_file is None:

        query = load_query(sys.stdin)

    else:

        with open(args.query_file, 'r') as query_file:
            query = load_query(query_file)

    augmentor = Augmentor(query)

    run(augmentor, args.command)


if __name__ == "__main__":
    main()
