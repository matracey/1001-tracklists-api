from typing import Any, Iterator, Literal
from urllib.parse import urljoin

from parsel import Selector

from common import dehumanize

from ..models.tracklist_result import TracklistResult
from .base_page_object import BasePageObject


class HomePageObject(BasePageObject):
    """
    A page object class for the home page.
    """

    __path__ = "/"

    __details_selector__: str = "details"
    __summary_selector__: str = "summary"
    __summary_text_selector__: str = f"{__summary_selector__}::text"
    __sidebar_section_titles_selector__: str = (
        f"{__details_selector__} > {__summary_text_selector__}"
    )
    __wrapped_row_class_selector__: str = ".wRow"

    def get_sidebar_sections(self) -> Iterator[str]:
        """
        Returns a list of sidebar sections.
        """
        for section in self._selector_.css(
            self.__sidebar_section_titles_selector__
        ).getall():
            yield section.strip()

    def get_section_lists(
        self, mode: Literal["json", "python"] = "python"
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Gets all of the sidebar sections and the tracklists associated with them.

        :param mode: The mode to return the data in. Can be either "json" or "python".

        :return: A dict of sidebar sections and their associated tracklists.
        """
        return {
            section: [tracklist.model_dump(mode=mode) for tracklist in tracklists]
            for section, tracklists in self.__fetch_sidebar_sections__().items()
        }

    def __fetch_sidebar_sections__(self) -> dict[str, list[TracklistResult]]:
        """
        Fetches all of the sidebar sections and the tracklists associated with them.

        :return: A dict of sidebar sections and associated TracklistResult objects.
        """
        sections = self._selector_.css(self.__details_selector__)
        result = {}

        for section in sections:
            section_name = section.css(self.__summary_text_selector__).get().strip()
            result[section_name] = [
                self.__parse_tracklist_row__(tracklist_row)
                for tracklist_row in section.css(self.__wrapped_row_class_selector__)
            ]

        return result

    def __parse_tracklist_row__(self, tracklist_row: Selector) -> TracklistResult:
        """
        Parses a tracklist row and returns a TracklistResult object.

        :param tracklist_row: The tracklist row Selector to parse.
        :return: A TracklistResult object.
        """
        anchor = tracklist_row.css("a")
        title = anchor.css("::text").get().strip()
        url = anchor.attrib["href"]

        views_str = tracklist_row.css("[title='tracklist views']::text").get().strip()
        date_str = tracklist_row.css("[title='tracklist date']::text").get().strip()
        attrs = [a.attrib["title"] for a in tracklist_row.css("i[title]")]

        return TracklistResult.model_validate(
            {
                "title": title,
                "url": urljoin(self.__base_url__, url),
                "view_count": dehumanize(views_str),
                "date": date_str,
                "attributes": attrs,
            }
        )
