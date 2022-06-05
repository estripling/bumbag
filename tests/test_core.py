import math
import operator

import pytest

from bumbag import core


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("no punctuation", "no punctuation"),
        (" text with whitespaces ", " text with whitespaces "),
        ("CAPITAL LETTERS", "CAPITAL LETTERS"),
        ("exclamation mark!", "exclamation mark"),
        ('quotation mark"', "quotation mark"),
        ("hash#", "hash"),
        ("dollar$", "dollar"),
        ("percentage%", "percentage"),
        ("ampersand&", "ampersand"),
        ("apostrophe'", "apostrophe"),
        ("asterix*", "asterix"),
        ("plus+", "plus"),
        ("comma,", "comma"),
        ("dash-", "dash"),
        ("period.", "period"),
        ("slash/", "slash"),
        ("colon:", "colon"),
        ("semicolon;", "semicolon"),
        ("less than sign<", "less than sign"),
        ("equal sign=", "equal sign"),
        ("greater than sign>", "greater than sign"),
        ("question mark?", "question mark"),
        ("at sign@", "at sign"),
        ("backslash\\", "backslash"),
        ("caret^", "caret"),
        ("underscore_", "underscore"),
        ("backtick`", "backtick"),
        ("vertical bar symbol|", "vertical bar symbol"),
        ("tilde~", "tilde"),
        ("(round brackets)", "round brackets"),
        ("{curly brackets}", "curly brackets"),
        ("[square brackets]", "square brackets"),
    ],
)
def test_remove_punctuation(arg, expected):
    actual = core.remove_punctuation(arg)
    assert actual == expected


@pytest.mark.parametrize("arg, expected", [(0, 1), (1, 2), (10, 11), (21, 22)])
def test_op(arg, expected):
    add1 = core.op(operator.add, 1)
    actual = add1(arg)
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
    f = core.sig(digits=digits)
    if digits < 1:
        with pytest.raises(ValueError):
            f(number)
    else:
        actual = f(number)
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
    ],
)
def test_extend_range(args, expected):
    vmin, vmax, pmin, pmax = args
    f = core.extend_range(pmin=pmin, pmax=pmax)
    if pmin < 0 or pmax < 0:
        with pytest.raises(ValueError):
            f(vmin, vmax)
    else:
        actual = f(vmin, vmax)
        assert actual == expected


def test_get_function_name():
    def my_test_function():
        return core.get_function_name()

    actual = my_test_function()
    expected = "my_test_function"
    assert actual == expected
