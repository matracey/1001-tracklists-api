"""
A module for the BaseCommand class.
"""

from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
from json import dumps
from re import compile as comp
from sys import exit as sysexit
from typing import Any, Optional

from ..command_arguments import OutputArgument


class BaseCommand(metaclass=ABCMeta):
    """
    A base class for any command.
    """

    __abc_error_message__ = "Not implemented by subclass."

    # noinspection PyPropertyDefinition
    @property
    @staticmethod
    @abstractmethod
    def __subcommand_dest__() -> str:
        """
        The destination for the subcommand.
        """
        raise NotImplementedError(BaseCommand.__abc_error_message__)

    # noinspection PyPropertyDefinition
    @property
    @staticmethod
    @abstractmethod
    def command_name() -> str:
        """
        The name of the command.
        """
        raise NotImplementedError(BaseCommand.__abc_error_message__)

    # noinspection PyPropertyDefinition
    @property
    @staticmethod
    @abstractmethod
    def command_help() -> str:
        """
        The help message for the command.
        """
        raise NotImplementedError(BaseCommand.__abc_error_message__)

    def __init__(self, parser: ArgumentParser, **args):
        self.__args__ = args
        self.__parser__ = parser

        self.__subcommand__ = args.pop(self.__subcommand_dest__)

        if not self.__subcommand__:
            parser.print_help()
            sysexit(1)

    @classmethod
    def build_subparser(cls, s) -> ArgumentParser:
        """
        Creates a subparser on the given subparsers object.

        :param s: The subparsers object.
        """
        parser: ArgumentParser = s.add_parser(cls.command_name, help=cls.command_help)

        return cls.build_parser(parser)

    # noinspection PyTypeChecker
    @classmethod
    @abstractmethod
    def build_parser(cls, parser: ArgumentParser) -> ArgumentParser:
        """
        Builds the parser for the command.

        :param parser: The argument parser.
        """
        cls.__subparsers__ = parser.add_subparsers(dest=cls.__subcommand_dest__)

        return parser

    @staticmethod
    def compile_re(key: str, **kwargs):
        """
        Compiles the regular expression pattern from the kwargs.

        :param key: The key to extract the regular expression pattern from.
        :param kwargs: The dictionary of keyword arguments.
        :return: The compiled regular expression pattern.
        """
        return comp(kwargs.get(key)) if kwargs.get(key) else None

    @classmethod
    def handle_output(
        cls,
        output: Optional[Any] = None,
        args: OutputArgument = None,
    ):
        """
        Handle the output of the command.

        :param output: The output to write.
        :param write_file: A boolean flag to write the output to a file.
        :param output_file: The name of the file to write the output to.
        """
        if not args:
            args = OutputArgument()
        args.command_name = cls.command_name

        str_out = (
            dumps(output, indent=2, ensure_ascii=False)
            if not isinstance(output, str)
            else output
        )

        if args.write_file and not args.output_file:
            args.output_file = args.default_output_file

        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(str_out)
        else:
            print(str_out)
