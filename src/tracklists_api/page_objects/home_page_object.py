from typing import Iterator
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

    def get_sidebar_sections(self) -> Iterator[str]:
        """
        Returns a list of sidebar sections.
        """
        for section in self._selector_.css(
            self.__sidebar_section_titles_selector__
        ).getall():
            yield section.strip()

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
