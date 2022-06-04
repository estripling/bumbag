import pytest


@pytest.fixture(scope="module")
def n10():
    return 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
