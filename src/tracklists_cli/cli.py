"""
Contains the entrypoints for the command line tool(s) in this package.
"""

from argparse import ArgumentParser


def main():
    """
    The main entrypoint for the command line tool.

    :return: None
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_subparsers(dest="subcommand")

    args = parser.parse_args()
    subcommand = args.subcommand
    delattr(args, "subcommand")

    if not subcommand:
        parser.print_help()
