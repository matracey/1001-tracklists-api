from typing import Iterator

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
