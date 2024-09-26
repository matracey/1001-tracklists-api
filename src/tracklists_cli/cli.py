"""
Contains the entrypoints for the command line tool(s) in this package.
"""

from argparse import ArgumentParser, Namespace
from typing import Optional, Tuple

from .commands import BaseCommand

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


def __parse_args_and_invoke__(
    module: BaseCommand,
    parser: Optional[ArgumentParser] = None,
    args: Optional[Namespace] = None,
):
    """
    Invokes the provided module with the provided arguments using the run_command function. If no
    arguments are provided, they are parsed using the module's build_parser function.

    :param module: The module to invoke. Should have run_command and build_parser functions
    :param args: The arguments to pass to the module
    :return: None
    """
    if args is None:
        parser, args = __parse_args__(module)
    module(parser, **vars(args))


def __parse_args__(module: BaseCommand) -> Tuple[ArgumentParser, Namespace]:
    """
    Parses the arguments for the provided module using the module's build_parser function.

    :param module: The module to parse arguments for. Should have a build_parser function
    :return: The parsed arguments as a Namespace
    """
    parser: ArgumentParser = __build_root_parser__(
        module.command_name, module.command_help
    )
    module.build_parser(parser)
    return parser, parser.parse_args()


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
