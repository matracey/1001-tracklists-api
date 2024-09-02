"""
A module for the BaseCommand class.
"""

from abc import ABCMeta
from argparse import ArgumentParser


class BaseCommand(metaclass=ABCMeta):
    """
    A base class for any command.
    """

    def __init__(self, parser: ArgumentParser, **args):
        self.__args__ = args
        self.__parser__ = parser
