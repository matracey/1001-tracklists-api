"""
A module for the BaseCommand class.
"""

from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
from datetime import datetime
from re import compile as comp
from sys import exit as sysexit


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

    @staticmethod
    def filesafe_datetime_now() -> str:
        """
        Get the current datetime in a file-safe format.
        """
        return "".join(
            c if (c.isalnum() or c in "._- ") else "_"
            for c in datetime.now().isoformat()
        )
