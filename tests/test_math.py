import pytest
import toolz

from bumbag import math


@pytest.mark.parametrize("n", [1, 2, 3, 10, 100])
@pytest.mark.parametrize("start", [-2, -1, 0, 1, 2])
def test_iseq(start, n):
    actual = tuple(toolz.take(n, math.iseq(start)))
    k = start + n
    r = range(start, k + 1) if start or start == n else range(start, k)
    expected = tuple(r)[:n]
    assert actual == expected
