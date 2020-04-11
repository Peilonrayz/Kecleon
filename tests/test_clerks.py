import pytest
import responses
from base import DATA, WrappedClerk, assert_equal, build_items, build_tmpdir
from kecleon import jobs


def build_mutable():
    with build_tmpdir() as location:
        yield (
            WrappedClerk(jobs.FileClerk(), str(location / "clerks" / "file")),
            build_items(DATA / "foo"),
            "foo bar baz",
        )
    with build_tmpdir() as location:
        yield (
            WrappedClerk(
                jobs.Zip7Clerk(warn=False), (str(location / "clerks" / "zip"), "foo")
            ),
            build_items(DATA / "foo.7z"),
            "foo bar baz",
        )


def build_immutable():
    yield (
        WrappedClerk(jobs.WebClerk(), "https://example.com/stream"),
        build_items(DATA / "foo"),
        "foo bar baz",
    )


def _build_cleck_tests(builder):
    for clerk, items, value in builder():
        for item in items:
            yield clerk, item, value


@responses.activate
def test_mutable_clerks():
    for clerk, item, value in _build_cleck_tests(build_mutable):
        assert not clerk.has_item()
        assert clerk.set(item) is None
        assert clerk.has_item()
        assert_equal(clerk.get().get_all(), value)
        assert_equal(list(clerk.get().get_stream()), value)
        assert clerk.has_item()
        assert clerk.delete() is None
        assert not clerk.has_item()


@responses.activate
def test_immutable_clerks():
    for clerk, item, value in _build_cleck_tests(build_immutable):
        assert clerk.has_item()
        assert_equal(clerk.get().get_all(), "foo bar baz")
        assert_equal(list(clerk.get().get_stream()), "foo bar baz")
        with pytest.raises(ValueError, match="Can't write to web resource"):
            clerk.set(item)
        with pytest.raises(ValueError, match="Can't delete web resource"):
            clerk.delete()


def test_zip7_warnings() -> None:
    """Test warnings work correctly."""
    jobs.Zip7Clerk(warn=False)
    with pytest.warns(
        UserWarning,
        match="ZipClerk's underlying datatype does not provide a streaming interface.",
    ):
        jobs.Zip7Clerk()
