import pytest
import toolz

from bumbag import math


@pytest.mark.parametrize("n", [1, 2, 3, 10, 100])
@pytest.mark.parametrize("start", ["invalid_type", -2, -1, 0, 1, 2])
@pytest.mark.parametrize("step", ["invalid_type", -1, -0.5, 0, 1, 2])
def test_iseq(start, step, n):
    types = (int, float)
    if not (isinstance(start, types) and isinstance(step, types)):
        with pytest.raises(TypeError):
            math.irange(start, step)

    elif step <= 0:
        with pytest.raises(ValueError):
            math.irange(start, step)

    else:
        actual = tuple(toolz.take(n, math.irange(start, step)))
        expected = tuple(range(start, 1000, step))[:n]
        assert actual == expected


@pytest.mark.parametrize("arg", [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_iseven(arg):
    actual = math.iseven(arg)
    expected = arg % 2 == 0
    assert actual == expected


@pytest.mark.parametrize("arg", [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_isodd(arg):
    actual = math.isodd(arg)
    is_even_number = arg % 2 == 0
    expected = not is_even_number
    assert actual == expected


def test_fibonacci():
    output = tuple(toolz.take(16, math.fibonacci()))
    expect = (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987)
    assert output == expect


@pytest.mark.parametrize(
    "arg, expected",
    [
        (-2, None),
        (-1, None),
        (0, None),
        (1, (1,)),
        (2, (2, 1)),
        (4, (4, 2, 1)),
        (7, (7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1)),
        (11, (11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1)),
        (12, (12, 6, 3, 10, 5, 16, 8, 4, 2, 1)),
    ],
)
def test_collatz(arg, expected):
    if arg < 1:
        with pytest.raises(ValueError):
            tuple(math.collatz(arg))
    else:
        actual = tuple(math.collatz(arg))
        assert actual == expected
