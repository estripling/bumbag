import pytest

import bumbag


def test_concat_strings():
    strings = ["Hello", "World"]
    actual = bumbag.concat_strings(strings)
    expected = " ".join(strings)
    assert actual == expected

    hyphen_concat = bumbag.concat_strings(sep="-")
    actual = hyphen_concat(strings)
    expected = "-".join(strings)
    assert actual == expected


def test_filter_regex(zen_of_python):
    filter_python_regex = bumbag.filter_regex("python")
    filter_better_regex = bumbag.filter_regex("better")

    actual = list(filter_python_regex(zen_of_python))
    expected = ["The Zen of Python, by Tim Peters"]
    assert actual == expected, "filter_python_regex fails"

    actual = list(filter_better_regex(zen_of_python))
    expected = [
        "Beautiful is better than ugly.",
        "Explicit is better than implicit.",
        "Simple is better than complex.",
        "Complex is better than complicated.",
        "Flat is better than nested.",
        "Sparse is better than dense.",
        "Now is better than never.",
        "Although never is often better than *right* now.",
    ]
    assert actual == expected, "filter_better_regex fails"


def test_headline():
    actual = bumbag.headline("Hello, World!", length=30)
    expected = "------- Hello, World! --------"
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (("hello", "hello"), "hello\n     \nhello"),
        (("hello", "hallo"), "hello\n |   \nhallo"),
        (("hello", "hell"), "hello\n    |\nhell"),
        (("hello", "hall"), "hello\n |  |\nhall"),
        (("hall", "hello"), "hall\n |  |\nhello"),
        (("1234", "11342"), "1234\n |  |\n11342"),
        (("1234.56", "1234,56"), "1234.56\n    |  \n1234,56"),
    ],
)
def test_highlight_string_differences(arg, expected):
    actual = bumbag.highlight_string_differences(*arg)
    assert actual == expected


def test_map_regex(zen_of_python):
    map_python_regex = bumbag.map_regex("python")
    map_better_regex = bumbag.map_regex("better")

    actual = list(map_python_regex(zen_of_python))
    expected = [["Python"]] + [[] for _ in range(19)]
    assert actual == expected, "map_python_regex fails"

    actual = list(map_better_regex(zen_of_python))
    expected = (
        [[]]
        + [["better"] for _ in range(6)]
        + [[] for _ in range(8)]
        + [["better"] for _ in range(2)]
        + [[] for _ in range(3)]
    )
    assert actual == expected, "map_better_regex fails"


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
        ("asterisk*", "asterisk"),
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
    actual = bumbag.remove_punctuation(arg)
    assert actual == expected
