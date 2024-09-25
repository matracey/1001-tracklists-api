"""
A module for the BaseCommand class.
"""

from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
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
