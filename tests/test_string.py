import pytest

from bumbag import string


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("no punctuation", "no punctuation"),
        (" string with whitespaces ", " string with whitespaces "),
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
    actual = string.remove_punctuation(arg)
    assert actual == expected


def test_map_regex(zen_of_python):
    map_python_regex = string.map_regex("python")
    map_better_regex = string.map_regex("better")

    actual = list(map_python_regex(zen_of_python))
    expected = [["Python"]] + [[] for _ in range(19)]
    assert actual == expected, "map_python_regex failed"

    actual = list(map_better_regex(zen_of_python))
    expected = (
        [[]]
        + [["better"] for _ in range(6)]
        + [[] for _ in range(8)]
        + [["better"] for _ in range(2)]
        + [[] for _ in range(3)]
    )
    assert actual == expected, "map_better_regex failed"
