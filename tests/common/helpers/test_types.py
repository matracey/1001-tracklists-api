# pylint: disable=missing-function-docstring

import pytest

from src.common import dehumanize


def test_dehumanize_should_handle_thousand_symbols():
    assert dehumanize("1k") == str(1_000)
    assert dehumanize("1.2k") == str(1_200)
