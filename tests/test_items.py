import contextlib
import math
from typing import AnyStr, Iterator

import pytest
import responses
from base import DATA, assert_equal, build_items, build_tmpdir
from kecleon import Item, base, jobs


def _build_item_tests():
    for fn in [
        lambda item: item.get_all(),
        lambda item: list(item.get_stream()),
    ]:
        for item in build_items(DATA / "foo"):
            yield fn, item, "foo bar baz"


@responses.activate
def test_items() -> None:
    for get_fn, item, value in _build_item_tests():
        assert_equal(get_fn(item), value)
        with pytest.raises(ValueError, match="has already been consumed"):
            item.get_all()
        with pytest.raises(ValueError, match="has already been consumed"):
            item.get_stream()


def test_raw_item_warnings() -> None:
    """Test warnings work correctly."""
    jobs.RawItem("foo bar baz", warn=False)
    with pytest.warns(
        UserWarning,
        match="RawItem's underlying datatype does not provide a streaming interface.",
    ):
        jobs.RawItem("foo bar baz")
