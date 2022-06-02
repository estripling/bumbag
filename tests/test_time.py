import types
from datetime import date

import pytest

from bumbag import time


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
