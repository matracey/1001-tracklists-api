from datetime import date

from pydantic_core import Url

from .base_schema import BaseSchema


class TracklistResult(BaseSchema):
    """
    A schema class for a tracklist result.
    """

    title: str
    """
    The title of the tracklist.
    """
    url: Url
    """
    The URL of the tracklist.
    """
    view_count: int
    """
    The view count of the tracklist.
    """
    date: date
    """
    The date of the tracklist.
    """
    attributes: list[str]
    """
    The attributes of the tracklist.
    """
