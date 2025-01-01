# pylint: disable=missing-function-docstring

import pytest

from src.common import dehumanize


def test_dehumanize_should_handle_thousand_symbols():
    assert dehumanize("1k") == str(1_000)
    assert dehumanize("1.2k") == str(1_200)


def test_dehumanize_should_handle_million_symbols():
    assert dehumanize("2m") == str(2_000_000)
    assert dehumanize("2.5m") == str(2_500_000)


def test_dehumanize_should_handle_billion_symbols():
    assert dehumanize("3b") == str(3_000_000_000)
    assert dehumanize("3.5b") == str(3_500_000_000)


def test_dehumanize_should_handle_commas():
    assert dehumanize("1,000") == str(1_000)
    assert dehumanize("1,000,000") == str(1_000_000)


def test_dehumanize_should_not_change_unhumanized_numbers():
    assert dehumanize("100") == str(100)
    assert dehumanize("1.23") == str(1.23)
