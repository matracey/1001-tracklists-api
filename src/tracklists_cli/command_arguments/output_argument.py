from argparse import ArgumentParser
from datetime import datetime
from typing import Optional

from pydantic import Field

from .base_argument import BaseArgument


class OutputArgument(BaseArgument):
    """
    A class for the Playwright argument.
    """

    write_file: bool = Field(default=False)
    """
    Write the results to a file.
    """
    output_file: Optional[str] = Field(default=None)
    """
    The output file to write the results to.
    """
    command_name: Optional[str] = Field(default=None)
    """
    The name of the command.
    """

    @property
    def default_output_file(self) -> str:
        """
        Get the default output file name.
        """
        return (
            f"{self.command_name}_{self.__filesafe_datetime_now__()}.json"
            if self.command_name
            else f"{self.__filesafe_datetime_now__()}.json"
        )

    @staticmethod
    def __filesafe_datetime_now__() -> str:
        """
        Get the current datetime in a file-safe format.
        """
        return "".join(
            c if (c.isalnum() or c in "._- ") else "_"
            for c in datetime.now().isoformat()
        )

    @staticmethod
    def add_arguments(parser: ArgumentParser) -> ArgumentParser:
        """
        Adds the properties of the dataclass type as arguments to the specified parser.

        :param parser: The parser to add the arguments to.
        :return: The parser with the added arguments.
        """

        OutputArgument.__add_superclass_arguments__(parser)

        if not OutputArgument.__has_dest__(parser, "write_file"):
            parser.add_argument(
                "-f",
                "--file",
                help="Write the results to a file. To specify the filename, use the -o option.",
                action="store_true",
                dest="write_file",
            )

        if not OutputArgument.__has_dest__(parser, "output_file"):
            parser.add_argument(
                "-o",
                "--output-file",
                help="The output file to write the results to.",
                type=str,
                default=None,
                dest="output_file",
            )

        return parser
