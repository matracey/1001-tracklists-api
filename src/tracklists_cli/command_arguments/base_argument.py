from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser, Namespace

from tracklists_api.models.base_schema import BaseSchema


class BaseArgument(BaseSchema, metaclass=ABCMeta):
    """
    A class for the base argument.
    """

    __abc_error_message__ = "Not implemented by subclass."

    @classmethod
    def from_kwargs(cls, **kwargs):
        """
        Converts the namespace to the dataclass type.

        :param namespace: The namespace to convert.
        :return: The converted dataclass type.
        """
        return cls.model_validate(kwargs, strict=False)

    @classmethod
    def from_namespace(cls, namespace: Namespace):
        """
        Converts the namespace to the dataclass type.

        :param namespace: The namespace to convert.
        :return: The converted dataclass type.
        """
        return cls.from_kwargs(**vars(namespace))

    @staticmethod
    @abstractmethod
    def add_arguments(parser: ArgumentParser) -> ArgumentParser:
        """
        Adds the properties of the dataclass type as arguments to the specified parser.

        :param parser: The parser to add the arguments to.
        :return: The parser with the added arguments.
        """

    @classmethod
    def __add_superclass_arguments__(cls, parser: ArgumentParser) -> ArgumentParser:
        """
        Adds the properties of the superclass as arguments to the specified parser.

        :param parser: The parser to add the arguments to.
        :return: The parser with the added arguments.
        """
        for superclass in cls.__bases__:
            if superclass == cls:
                continue
            if hasattr(superclass, "add_arguments"):
                superclass.add_arguments(parser)
        return parser

    @staticmethod
    def __has_dest__(parser: ArgumentParser, dest: str) -> bool:
        """
        Check if the parser has a destination with the specified name.

        :param parser: The parser to check.
        :param dest: The destination name to check for.
        :return: True if the destination exists; otherwise, False.
        """
        # pylint: disable=protected-access
        return any(action.dest == dest for action in parser._actions)
