from importlib.metadata import version

import bumbag


def test_version():
    assert bumbag.__version__ == version("bumbag")
