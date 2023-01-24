from importlib import metadata

import bumbag


def test_version():
    assert bumbag.__version__ == metadata.version("bumbag")
