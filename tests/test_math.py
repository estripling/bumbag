import pytest
import toolz

from bumbag import math


@pytest.mark.parametrize("len_seq", [1, 2, 3, 10, 100])
@pytest.mark.parametrize("arg", [-2, -1, 0, 1, 2])
def test_iseq(arg, len_seq):
    actual = tuple(toolz.take(len_seq, math.iseq(arg)))
    k = arg + len_seq
    r = range(arg, k + 1) if arg or arg == len_seq else range(arg, k)
    expected = tuple(r)[:len_seq]
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


def test_iseq_even():
    output = tuple(toolz.take(10, math.iseq_even(1)))
    expect = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
    assert output == expect


def test_iseq_odd():
    output = tuple(toolz.take(10, math.iseq_odd(1)))
    expect = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19)
    assert output == expect


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


def test_two_set_summary():
    x = {"a", "c", "b", "g", "h"}
    y = {"c", "d", "e", "f", "g"}
    summary = math.two_set_summary(x, y)

    assert isinstance(summary, dict)
    assert summary["x"] == x
    assert summary["y"] == y
    assert summary["x | y"] == x.union(y)
    assert summary["x & y"] == x.intersection(y)
    assert summary["x - y"] == x.difference(y)
    assert summary["y - x"] == y.difference(x)
    assert summary["x ^ y"] == x.symmetric_difference(y)
    assert summary["jaccard"] == 0.25
    assert summary["overlap"] == 0.4
    assert summary["disjoint?"] is False
    assert summary["x == y"] is False
    assert summary["x <= y"] is False
    assert summary["x <  y"] is False
    assert summary["y <= x"] is False
    assert summary["y <  x"] is False

    lines = [
        "    x (n=5): {'a', 'b', 'c', ...}",
        "    y (n=5): {'c', 'd', 'e', ...}",
        "x | y (n=8): {'a', 'b', 'c', ...}",
        "x & y (n=2): {'c', 'g'}",
        "x - y (n=3): {'a', 'b', 'h'}",
        "y - x (n=3): {'d', 'e', 'f'}",
        "x ^ y (n=6): {'a', 'b', 'd', ...}",
        "jaccard = 0.25",
        "overlap = 0.4",
        "disjoint?: False",
        "x == y: False",
        "x <= y: False",
        "x <  y: False",
        "y <= x: False",
        "y <  x: False",
    ]
    report = "\n".join(lines)
    assert summary["report"] == report
