import pytest
from kecleon import FileClerk, Store
from kecleon.jobs import RawItem
from kecleon.store import Clerks
from state import tmpdir


def test_store_constructor():
    value = {
        "foo": FileClerk(),
        "bar": FileClerk(),
    }
    assert Store(value).clerks.clerks == value
    assert Store(foo=FileClerk(), bar=FileClerk(),).clerks.clerks == value
    assert Store({"foo": FileClerk()}, bar=FileClerk(),).clerks.clerks == value
    assert Store(Clerks({"foo": FileClerk()}), bar=FileClerk(),).clerks.clerks == value
    assert (
        Store(Clerks({"foo": FileClerk(), "bar": FileClerk(),})).clerks.clerks == value
    )


def test_store_exceptions():
    store = Store(foo=FileClerk(), bar=FileClerk(),)

    with tmpdir() as location:
        line = store.line(foo=str(location / "foo"), bar=str(location / "bar"),)

        with pytest.raises(ValueError, match="Item is unavailable"):
            line.get()

        with pytest.raises(TypeError, match="must be supplied one keyword argument"):
            line.set()

        with pytest.raises(TypeError, match="must be supplied one keyword argument"):
            line.set(foo=None, bar=None)

        with pytest.raises(TypeError, match="got an unexpected keyword argument: baz"):
            line.delete("baz")


def test_store():
    store = Store(foo=FileClerk(), bar=FileClerk(),)

    with tmpdir() as location:
        line = store.line(foo=str(location / "foo"), bar=str(location / "bar"),)

        item = line.set(bar=RawItem("foo bar baz", warn=False))
        assert item.get_all() == "foo bar baz"
        assert line.get().get_all() == "foo bar baz"
        item = store.get(foo=str(location / "foo"), bar=str(location / "bar"),)
        assert item.get_all() == "foo bar baz"
        assert line.delete("foo") is None
        assert line.get().get_all() == "foo bar baz"
        assert line.delete("bar") is None
        with pytest.raises(ValueError, match="Item is unavailable"):
            line.get()
