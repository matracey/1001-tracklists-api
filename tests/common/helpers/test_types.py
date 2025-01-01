# pylint: disable=missing-function-docstring

import pytest

from src.common import dehumanize


def test_dehumanize_should_handle_thousand_symbols():
    assert dehumanize("1k") == str(1_000)
    assert dehumanize("1.2k") == str(1_200)


def test_dehumanize_should_handle_million_symbols():
    assert dehumanize("2m") == str(2_000_000)
    assert dehumanize("2.5m") == str(2_500_000)
