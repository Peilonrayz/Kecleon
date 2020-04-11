import contextlib
import math
import pathlib
from typing import AnyStr, Generic, Iterator, TypeVar, Union

import requests
import responses
from kecleon import Clerk, FileClerk, Item, base, jobs
from state import tmpdir

T = TypeVar("T")
Response = Union[AnyStr, Iterator[AnyStr]]

DATA = pathlib.Path(__file__).resolve().parent / "data"


class RawItem(base.Item):
    """Raw item that doesn't overload _get_all."""

    _text: AnyStr

    def __init__(self, text: AnyStr, warn: bool = True) -> None:
        """Initialize a raw item."""
        super().__init__()
        self._text = text

    def _get_stream(self) -> Iterator[AnyStr]:
        """Get raw text as a stream."""
        for i in range(int(math.ceil(len(self._text) / 1024))):
            yield self._text[i * 1024 : (i + 1) * 1024]


class WrappedClerk(Generic[T]):
    _clerk: Clerk
    _value: T

    def __init__(self, clerk: Clerk, value: T) -> None:
        self._clerk = clerk
        self._value = value

    def has_item(self) -> bool:
        return self._clerk.has_item(self._value)

    def get(self) -> Item:
        return self._clerk.get(self._value)

    def set(self, item: Item) -> None:
        return self._clerk.set(self._value, item)

    def delete(self) -> None:
        return self._clerk.delete(self._value)


@contextlib.contextmanager
def build_tmpdir() -> Iterator[pathlib.Path]:
    with tmpdir() as location:
        yield location


def build_items(location: pathlib.Path) -> Iterator[Item]:
    try:
        value = location.read_text()
    except UnicodeDecodeError:
        value = location.read_bytes()
        strings = False
    else:
        strings = True

    responses.add(
        responses.GET,
        "https://example.com/stream",
        body=value,
        status=200,
        stream=True,
    )

    if strings:
        yield RawItem(value)
        yield jobs.RawItem(value, warn=False)
        yield jobs.FileItem(location.open())

    # Bytes
    value = location.read_bytes()
    yield RawItem(value)
    yield jobs.RawItem(value, warn=False)
    yield jobs.FileItem(location.open("rb"))
    if strings:
        yield jobs.WebItem(requests.get("https://example.com/stream", stream=True))


def convert_expected(actual: Response, expected: str) -> Response:
    is_list = isinstance(actual, list)
    if isinstance(actual[0] if is_list else actual, bytes):
        expected = bytes(expected, encoding="utf-8")
    if not is_list:
        return expected
    start = 0
    ret = []
    for chunk in actual:
        end = start + len(chunk)
        ret.append(expected[start:end])
        start = end
    return ret


def assert_equal(actual: Response, expected: str) -> None:
    assert actual == convert_expected(actual, expected)
