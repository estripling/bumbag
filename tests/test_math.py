import pytest
import toolz

import bumbag


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
            tuple(bumbag.collatz(arg))
    else:
        actual = tuple(bumbag.collatz(arg))
        assert actual == expected


def test_fibonacci():
    actual = tuple(toolz.take(16, bumbag.fibonacci()))
    expected = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610)
    assert actual == expected


@pytest.mark.parametrize("arg", [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_iseven(arg):
    actual = bumbag.iseven(arg)
    expected = arg % 2 == 0
    assert actual == expected


@pytest.mark.parametrize("arg", [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_isodd(arg):
    actual = bumbag.isodd(arg)
    is_even_number = arg % 2 == 0
    expected = not is_even_number
    assert actual == expected
