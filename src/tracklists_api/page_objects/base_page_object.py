from abc import ABCMeta
from typing import Optional
from urllib.parse import urljoin

import requests
from parsel import Selector


class BasePageObject(metaclass=ABCMeta):
    """
    A base class for all PageObject classes.
    """

    __base_url__: str = "https://www.1001tracklists.com/"
    """
    The base URL for the page object.
    """

    __abc_error_message__ = "Not implemented by subclass."
    """
    The error message for abstract methods.
    """

    __path__: str = None
    """
    The path to the page object.
    """

    __timeout__: int
    """
    The timeout for requests, in seconds.
    """

    __selector__: Optional[Selector] = None

    @property
    def _selector_(self) -> Selector:
        """
        The Parsel selector for the page object.
        """
        if not self.__selector__:
            self.__load__()
        return self.__selector__

    @property
    def __page_url__(self) -> str:
        """
        The URL of the page object.

        :return: The URL of the page object.
        """
        return urljoin(self.__base_url__, self.__path__)

    def __init__(self, timeout: int = 10):
        """
        Initializes the PageObject with the given path and timeout.

        :param path: The path to the page object.
        :param timeout: The timeout for requests, in seconds.
        """
        self.__timeout__ = timeout

    def __load__(self):
        """
        Fetches the page URL using requests and initializes Parsel.
        """
        with requests.get(self.__page_url__, timeout=self.__timeout__) as response:
            self.__selector__ = Selector(response.text)
