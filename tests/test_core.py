import math
import operator

import pytest

import bumbag


@pytest.mark.parametrize(
    "x, expected",
    [
        (60, True),
        (9, False),
    ],
)
def test_all_predicate_true(x, expected):
    is_divisible_by_3_and_5 = bumbag.all_predicate_true(
        [lambda n: n % 3 == 0, lambda n: n % 5 == 0]
    )
    actual = is_divisible_by_3_and_5(x)
    assert actual == expected


@pytest.mark.parametrize(
    "x, expected",
    [
        (60, True),
        (9, True),
        (13, False),
    ],
)
def test_any_predicate_true(x, expected):
    is_divisible_by_3_or_5 = bumbag.any_predicate_true(
        [lambda n: n % 3 == 0, lambda n: n % 5 == 0]
    )
    actual = is_divisible_by_3_or_5(x)
    assert actual == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ((0, 1, -0.1, 0.1), None),
        ((0, 1, 0.1, -0.1), None),
        ((0, 1, -0.1, -0.1), None),
        ((0, 1, 0.0, 0.0), (0, 1)),
        ((0, 1, 0.05, 0.05), (-0.05, 1.05)),
        ((0, 1, 0.1, 0.1), (-0.1, 1.1)),
        ((0, 1, 0.05, 0.1), (-0.05, 1.1)),
        ((0, 1, 0.1, 0.05), (-0.1, 1.05)),
        ((-1, 10, 0.1, 0.1), (-2.1, 11.1)),
        ((0, 10, 0.1, 0.1), (-1.0, 11.0)),
        ((1, 0, -0.1, 0.1), None),
        ((1, 0, 0.05, 0.05), (-0.05, 1.05)),
    ],
)
def test_extend_range(args, expected):
    min_value, max_value, min_factor, max_factor = args
    f = bumbag.extend_range(min_factor=min_factor, max_factor=max_factor)
    if min_factor < 0 or max_factor < 0:
        with pytest.raises(ValueError):
            f(min_value, max_value)
    else:
        actual = f(min_value, max_value)
        assert actual == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ((1, 2, 3, 4, 5, 6), [1, 2, 3, 4, 5, 6]),
        (range(1, 7), [1, 2, 3, 4, 5, 6]),
        ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]),
        ([[], [1, 2], [3, 4, 5], [6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 2], 3, (4, 5), (6,)], [1, 2, 3, 4, 5, 6]),
        ([[[1, 2]], [3], 4, [[[5]]], [[[[6]]]]], [1, 2, 3, 4, 5, 6]),
        ([1, [2, 3, 4], [[5, 6]]], [1, 2, 3, 4, 5, 6]),
        ([1, [2, 3, 4, 5], 6, []], [1, 2, 3, 4, 5, 6]),
        ([[1, 2], [3, 4, 5], 6], [1, 2, 3, 4, 5, 6]),
        (([[1, 2], [3, 4, 5], 6],), [1, 2, 3, 4, 5, 6]),
        ([iter([1, (2, 3)]), 4, [], iter([[[5]], 6])], [1, 2, 3, 4, 5, 6]),
        (
            [["one", 2], 3, [4, "five"], ["six"]],
            ["one", 2, 3, 4, "five", "six"],
        ),
        (map(lambda x: 2 * x, range(1, 7)), [2, 4, 6, 8, 10, 12]),
        ((2 * x for x in range(1, 7)), [2, 4, 6, 8, 10, 12]),
        (tuple(2 * x for x in range(1, 7)), [2, 4, 6, 8, 10, 12]),
        (list(2 * x for x in range(1, 7)), [2, 4, 6, 8, 10, 12]),
        (([-1], 0, range(1, 7)), [-1, 0, 1, 2, 3, 4, 5, 6]),
        (([-1], 0, map(lambda x: 2 * x, range(1, 4))), [-1, 0, 2, 4, 6]),
        (([-1], 0, (2 * x for x in range(1, 4))), [-1, 0, 2, 4, 6]),
        (([-1], 0, tuple(2 * x for x in range(1, 4))), [-1, 0, 2, 4, 6]),
        (([-1], 0, list(2 * x for x in range(1, 4))), [-1, 0, 2, 4, 6]),
        (filter(lambda x: x % 2 == 0, range(1, 7)), [2, 4, 6]),
        ((-1, filter(lambda x: x % 2 == 0, range(1, 7))), [-1, 2, 4, 6]),
        (([-1], filter(lambda x: x % 2 == 0, range(1, 7))), [-1, 2, 4, 6]),
    ],
)
def test_flatten(args, expected):
    seqs = args
    actual = list(bumbag.flatten(seqs))
    assert actual == expected


@pytest.mark.parametrize(
    "x, expected_order",
    [
        (["a", "c", "b", "g", "h", "a", "g", "a"], ["a", "g", "c", "b", "h"]),
        (
            ["a", "c", None, "g", "h", "a", "g", "a"],
            ["a", "g", "c", None, "h"],
        ),
        (["a", 1, None, "g", "h", "a", "g", "a"], ["a", "g", 1, None, "h"]),
        (["a", 1, None, "g", 2.0, "a", "g", "a"], ["a", "g", 1, None, 2.0]),
        ([5, 2, True, "g", False, 5, "g", 5], [5, "g", 2, True, False]),
        ([1, 3, 2, 4, 8, 1, 4, 1], [1, 4, 3, 2, 8]),
    ],
)
def test_freq(x, expected_order):
    actual = bumbag.freq(x)
    assert isinstance(actual, dict)

    v1, v2, v3, v4, v5 = expected_order
    expected_frequency = {v1: 3, v2: 2, v3: 1, v4: 1, v5: 1}
    expected_cumulative_frequency = {v1: 3, v2: 5, v3: 6, v4: 7, v5: 8}
    expected_relative = {v1: 0.375, v2: 0.25, v3: 0.125, v4: 0.125, v5: 0.125}
    expected_cumulative_relative = {
        v1: 0.375,
        v2: 0.625,
        v3: 0.75,
        v4: 0.875,
        v5: 1.0,
    }

    assert list(actual["n"]) == expected_order
    assert actual["n"] == expected_frequency
    assert actual["N"] == expected_cumulative_frequency
    assert actual["r"] == expected_relative
    assert actual["R"] == expected_cumulative_relative


def test_get_function_name():
    def my_test_function():
        return bumbag.get_function_name()

    actual = my_test_function()
    expected = "my_test_function"
    assert actual == expected


def test_get_source_code():
    def my_test_function():
        return "Hello, World!"

    actual = bumbag.get_source_code(my_test_function)
    expected = '    def my_test_function():\n        return "Hello, World!"\n'
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (1, "1"),
        (10, "10"),
        (100, "100"),
        (1000, "1_000"),
        (1000000, "1_000_000"),
        (100000.0, "100_000.0"),
    ],
)
def test_numberformat(arg, expected):
    actual = bumbag.numberformat(arg)
    assert actual == expected


@pytest.mark.parametrize("arg, expected", [(0, 1), (1, 2), (10, 11), (21, 22)])
def test_op(arg, expected):
    inc = bumbag.op(operator.add, 1)
    actual = inc(arg)
    assert actual == expected


@pytest.mark.parametrize(
    "func, expected",
    [
        (set.intersection, {2}),
        (set.union, {0, 1, 2, 3, 4, 6, 8}),
        (set.difference, {0, 1, 3}),
        (set.symmetric_difference, {0, 1, 2, 3, 4, 8}),
    ],
)
def test_setred(func, expected):
    x = {0, 1, 2, 3}
    y = {2, 4, 6}
    z = {2, 6, 8}

    actual = bumbag.setred(func, x, y, z)
    assert actual == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ((math.inf, 3), math.inf),
        ((1234, 0), None),
        ((0, 3), 0),
        ((0.0, 3), 0.0),
        ((1e-12, 3), 1e-12),
        ((987654321.123456789, 1), 1000000000.0),
        ((987654321.123456789, 2), 990000000.0),
        ((987654321.123456789, 3), 988000000.0),
        ((987654321.123456789, 4), 987700000.0),
        ((987654321.123456789, 5), 987650000.0),
        ((987654321.123456789, 6), 987654000.0),
        ((987654321.123456789, 7), 987654300.0),
        ((987654321.123456789, 8), 987654320.0),
        ((987654321.123456789, 9), 987654321.0),
        ((987654321.123456789, 10), 987654321.1),
        ((987654321.123456789, 11), 987654321.12),
        ((987654321.123456789, 12), 987654321.123),
        ((987654321.123456789, 13), 987654321.1235),
        ((1.123456789, 1), 1.0),
        ((1.123456789, 2), 1.1),
        ((1.123456789, 3), 1.12),
        ((1.123456789, 4), 1.123),
        ((0.123456789, 1), 0.1),
        ((0.123456789, 2), 0.12),
        ((0.123456789, 3), 0.123),
        ((0.123456789, 4), 0.1235),
        ((1234, 1), 1000),
        ((1234, 2), 1200),
        ((1234, 3), 1230),
        ((1234, 4), 1234),
        ((-1.4142135623730951, 1), -1.0),
        ((-1.4142135623730951, 2), -1.4),
        ((-1.4142135623730951, 3), -1.41),
        ((-1.4142135623730951, 4), -1.414),
        ((14393237.76, 1), 10000000.0),
        ((14393237.76, 2), 14000000.0),
        ((14393237.76, 3), 14400000.0),
        ((14393237.76, 4), 14390000.0),
    ],
)
def test_sig(args, expected):
    number, digits = args
    f = bumbag.sig(digits=digits)
    if digits < 1:
        with pytest.raises(ValueError):
            f(number)
    else:
        actual = f(number)
        assert actual == expected


def test_two_set_summary():
    x = {"a", "c", "b", "g", "h"}
    y = {"c", "d", "e", "f", "g"}
    summary = bumbag.two_set_summary(x, y)

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
    assert summary["dice"] == 0.4
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
        "dice = 0.4",
        "disjoint?: False",
        "x == y: False",
        "x <= y: False",
        "x <  y: False",
        "y <= x: False",
        "y <  x: False",
    ]
    report = "\n".join(lines)
    assert summary["report"] == report
