import contextlib
import os
import pathlib
import tempfile


@contextlib.contextmanager
def tmpdir():
    with tempfile.TemporaryDirectory() as f:
        yield pathlib.Path(f)
