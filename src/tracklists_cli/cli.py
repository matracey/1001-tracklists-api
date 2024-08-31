"""
Contains the entrypoints for the command line tool(s) in this package.
"""

from argparse import ArgumentParser
from typing import Optional

CLI_NAME = "jobHelpers"
CLI_DESCRIPTION = (
    "A collection of tools to help with job application submission and management."
)


def __build_root_parser__(
    prog: Optional[str] = None, description: Optional[str] = None
) -> ArgumentParser:
    """
    Builds the root parser for the command line tool. All commands should inherit from this parser.

    :param prog: The name of the program.
    :param description: The description of the program.
    :return: The root parser
    """
    parser = ArgumentParser(
        prog=prog or CLI_NAME, description=description or CLI_DESCRIPTION
    )
    return parser


def main():
    """
    The main entrypoint for the command line tool.

    :return: None
    """
    parser: ArgumentParser = __build_root_parser__()
    parser.add_subparsers(dest="subcommand")

    args = parser.parse_args()
    subcommand = args.subcommand
    delattr(args, "subcommand")

    if not subcommand:
        parser.print_help()
