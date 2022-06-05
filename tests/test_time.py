import types
from datetime import date

import pytest

from bumbag import time


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("2022-01-01", date(2022, 1, 1)),
        ("2022-01-31", date(2022, 1, 31)),
    ],
)
def test_str_to_date(arg, expected):
    actual = time.str_to_date(arg)
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (date(2022, 1, 1), "2022-01-01"),
        (date(2022, 1, 31), "2022-01-31"),
    ],
)
def test_date_to_str(arg, expected):
    actual = time.date_to_str(arg)
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (date(2022, 1, 1), date(2022, 1, 31)),
        (date(2022, 2, 1), date(2022, 2, 28)),
        (date(2022, 3, 1), date(2022, 3, 31)),
        (date(2022, 4, 1), date(2022, 4, 30)),
        (date(2022, 5, 1), date(2022, 5, 31)),
        (date(2022, 6, 1), date(2022, 6, 30)),
        (date(2022, 7, 1), date(2022, 7, 31)),
        (date(2022, 8, 1), date(2022, 8, 31)),
        (date(2022, 9, 1), date(2022, 9, 30)),
        (date(2022, 10, 1), date(2022, 10, 31)),
        (date(2022, 11, 1), date(2022, 11, 30)),
        (date(2022, 12, 1), date(2022, 12, 31)),
        (date(1970, 1, 1), date(1970, 1, 31)),
        (date(1970, 1, 15), date(1970, 1, 31)),
        (date(1970, 1, 31), date(1970, 1, 31)),
        (date(2020, 2, 2), date(2020, 2, 29)),
        (date(2022, 2, 3), date(2022, 2, 28)),
        (date(2000, 2, 4), date(2000, 2, 29)),
        (date(1900, 2, 5), date(1900, 2, 28)),
        (date(2012, 2, 27), date(2012, 2, 29)),
        (date(2012, 2, 28), date(2012, 2, 29)),
        (date(2012, 2, 29), date(2012, 2, 29)),
    ],
)
def test_get_last_date_of_month(arg, expected):
    actual = time.get_last_date_of_month(arg.year, arg.month)
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (2008, True),
        (2012, True),
        (2016, True),
        (2020, True),
        (2022, False),
        (2024, True),
        (2000, True),
        (2001, False),
        (1900, False),
        (2100, False),
    ],
)
def test_is_leap_year(arg, expected):
    actual = time.is_leap_year(arg)
    assert actual == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            (date(2022, 1, 1), date(2022, 1, 5)),
            (
                date(2022, 1, 1),
                date(2022, 1, 2),
                date(2022, 1, 3),
                date(2022, 1, 4),
                date(2022, 1, 5),
            ),
        ),
    ],
)
def test_daterange(args, expected):
    start, end = args

    output = time.daterange(start, end)
    assert isinstance(output, types.GeneratorType)

    actual = tuple(output)
    assert actual == expected, "include start and end failed"

    actual = tuple(time.daterange(start, end, exclude_start=True))
    assert actual == expected[1:], "exclude start failed"

    actual = tuple(time.daterange(start, end, exclude_end=True))
    assert actual == expected[:-1], "exclude end failed"

    actual = tuple(time.daterange(start, end, True, True))
    assert actual == expected[1:-1], "exclude start and end failed"


@pytest.mark.parametrize(
    "arg, expected",
    [
        (-2.0, None),
        (-1, None),
        (0, "0 seconds"),
        (1, "1 second"),
        (59, "59 seconds"),
        (60, "1 minute"),
        (61, "1 minute, 1 second"),
        (120, "2 minutes"),
        (60 * 60, "1 hour"),
        (60 * 60 * 24, "1 day"),
        (110.0, "1 minute, 50 seconds"),
        (1.4142135623730951, "1.414214 seconds"),
        (60 * 60 * 24 + 123456, "2 days, 10 hours, 17 minutes"),
    ],
)
def test_humantime(arg, expected):
    if arg < 0:
        with pytest.raises(ValueError):
            time.humantime(arg)
    else:
        actual = time.humantime(arg)
        assert actual == expected
