import types
from datetime import date

import pytest
import toolz

from bumbag import time


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("2022-01-01", date(2022, 1, 1)),
        ("2022-01-31", date(2022, 1, 31)),
    ],
)
def test_to_date(arg, expected):
    actual = time.to_date(arg)
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (date(2022, 1, 1), "2022-01-01"),
        (date(2022, 1, 31), "2022-01-31"),
    ],
)
def test_to_str(arg, expected):
    actual = time.to_str(arg)
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
def test_last_date_of_month(arg, expected):
    actual = time.last_date_of_month(arg.year, arg.month)
    assert actual == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        ((date(2022, 8, 1), date(2022, 8, 1), False), 0),
        ((date(2022, 8, 1), date(2022, 8, 1), True), 1),
        ((date(2022, 8, 1), date(2022, 8, 7), False), 6),
        ((date(2022, 8, 7), date(2022, 8, 1), False), 6),
        ((date(2022, 8, 1), date(2022, 8, 7), True), 7),
        ((date(2022, 8, 7), date(2022, 8, 1), True), 7),
        ((date(2014, 1, 1), date(2016, 5, 6), False), 856),
    ],
)
def test_days_between_dates(args, expected):
    date1, date2, include_last_date = args
    actual = time.days_between_dates(date1, date2, include_last_date)
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
        (
            (date(2022, 1, 5), date(2022, 1, 1)),
            (
                date(2022, 1, 1),
                date(2022, 1, 2),
                date(2022, 1, 3),
                date(2022, 1, 4),
                date(2022, 1, 5),
            ),
        ),
        ((date(2022, 1, 1), date(2022, 1, 1)), (date(2022, 1, 1),)),
    ],
)
def test_daterange(args, expected):
    start, end = args

    actual = tuple(time.daterange(start, end))
    assert actual == expected, "including start and end dates fails"

    actual = tuple(time.daterange(start, end, include_start=False))
    assert actual == expected[1:], "excluding start date fails"

    actual = tuple(time.daterange(start, end, include_end=False))
    assert actual == expected[:-1], "excluding end date fails"

    actual = tuple(time.daterange(start, end, False, False))
    assert actual == expected[1:-1], "excluding start and end dates fails"


def test_drange():
    d1 = date(2022, 1, 1)

    actual = toolz.pipe(time.drange(d1, True), toolz.curried.take(3), list)
    expected = [date(2022, 1, 1), date(2022, 1, 2), date(2022, 1, 3)]
    assert actual == expected, "forward generation fails"

    actual = toolz.pipe(time.drange(d1, False), toolz.curried.take(3), list)
    expected = [date(2022, 1, 1), date(2021, 12, 31), date(2021, 12, 30)]
    assert actual == expected, "backward generation fails"


@pytest.mark.parametrize(
    "args, expected",
    [
        ((date(2022, 1, 1), 0), date(2022, 1, 1)),
        ((date(2022, 1, 1), 3), date(2022, 1, 3)),
        ((date(2022, 1, 1), -3), date(2021, 12, 30)),
        ((date(2022, 8, 1), 7), date(2022, 8, 7)),
        ((date(2022, 8, 7), -7), date(2022, 8, 1)),
        ((date(2022, 8, 8), -7), date(2022, 8, 2)),
        ((date(2022, 8, 1), 31), date(2022, 8, 31)),
        ((date(2022, 2, 1), 28), date(2022, 2, 28)),
        ((date(2022, 2, 1), 29), date(2022, 3, 1)),
        ((date(2020, 2, 1), 28), date(2020, 2, 28)),
        ((date(2020, 2, 1), 29), date(2020, 2, 29)),
        ((date(2020, 2, 1), 30), date(2020, 3, 1)),
    ],
)
def test_datedelta(args, expected):
    reference_date, days = args

    relative_date = time.datedelta(reference_date, days)
    assert relative_date == expected, "relative date does not match expected"

    n_days = toolz.count(time.daterange(reference_date, relative_date))
    n_days_expected = 1 if days == 0 else abs(days)
    assert n_days == n_days_expected, "number of days does not match expected"


@pytest.mark.parametrize(
    "args, expected",
    [
        ((date(2022, 8, 1), date(2022, 8, 1), False), 0),
        ((date(2022, 8, 1), date(2022, 8, 1), True), 1),
        ((date(2022, 8, 1), date(2022, 8, 7), False), 0),
        ((date(2022, 8, 7), date(2022, 8, 1), False), 0),
        ((date(2022, 8, 1), date(2022, 8, 7), True), 1),
        ((date(2022, 8, 7), date(2022, 8, 1), True), 1),
        ((date(2022, 1, 1), date(2022, 8, 1), False), 7),
        ((date(2022, 1, 1), date(2022, 8, 1), True), 8),
        ((date(2022, 1, 1), date(2022, 8, 31), False), 7),
        ((date(2022, 1, 1), date(2022, 8, 31), True), 8),
        ((date(2022, 1, 31), date(2022, 8, 31), False), 7),
        ((date(2022, 1, 31), date(2022, 8, 31), True), 8),
        ((date(2022, 8, 31), date(2022, 1, 31), False), 7),
        ((date(2022, 8, 31), date(2022, 1, 31), True), 8),
        ((date(2022, 1, 15), date(2022, 8, 15), False), 7),
        ((date(2022, 1, 15), date(2022, 8, 15), True), 8),
        ((date(2022, 8, 15), date(2022, 1, 15), False), 7),
        ((date(2022, 8, 15), date(2022, 1, 15), True), 8),
        ((date(2022, 1, 1), date(2022, 1, 31), False), 0),
        ((date(2022, 1, 1), date(2022, 2, 1), False), 1),
        ((date(2020, 2, 1), date(2020, 2, 28), False), 0),
        ((date(2020, 2, 1), date(2020, 2, 29), False), 0),
        ((date(2020, 2, 1), date(2020, 3, 1), False), 1),
        ((date(2020, 2, 29), date(2020, 3, 1), False), 0),
        ((date(2020, 2, 28), date(2020, 3, 1), False), 0),
        ((date(2020, 2, 15), date(2020, 3, 1), False), 0),
        ((date(2020, 2, 2), date(2020, 3, 1), False), 0),
        ((date(2020, 2, 2), date(2020, 3, 2), False), 1),
        ((date(2019, 12, 1), date(2020, 2, 1), False), 2),
        ((date(2019, 12, 2), date(2020, 2, 1), False), 1),
        ((date(2019, 12, 31), date(2020, 2, 1), False), 1),
        ((date(2020, 1, 1), date(2020, 2, 1), False), 1),
        ((date(2020, 1, 2), date(2020, 2, 1), False), 0),
        ((date(2020, 3, 1), date(2020, 4, 1), False), 1),
        ((date(2020, 3, 2), date(2020, 4, 1), False), 0),
        ((date(2020, 4, 1), date(2020, 5, 1), False), 1),
        ((date(2020, 4, 2), date(2020, 5, 1), False), 0),
        ((date(2020, 4, 15), date(2020, 5, 1), False), 0),
        ((date(2020, 4, 15), date(2020, 5, 14), False), 0),
        ((date(2020, 4, 15), date(2020, 5, 15), False), 1),
        ((date(2020, 4, 15), date(2020, 5, 16), False), 1),
        ((date(2020, 1, 1), date(2022, 1, 1), False), 24),
        ((date(2020, 1, 1), date(2022, 2, 1), False), 25),
    ],
)
def test_months_between_dates(args, expected):
    date1, date2, include_last_date = args
    actual = time.months_between_dates(date1, date2, include_last_date)
    assert actual == expected


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            (date(2022, 1, 1), date(2022, 4, 30)),
            (
                date(2022, 1, 1),
                date(2022, 2, 1),
                date(2022, 3, 1),
                date(2022, 4, 1),
            ),
        ),
        (
            (date(2022, 1, 1), date(2022, 4, 1)),
            (
                date(2022, 1, 1),
                date(2022, 2, 1),
                date(2022, 3, 1),
                date(2022, 4, 1),
            ),
        ),
        (
            (date(2022, 4, 30), date(2022, 1, 31)),
            (
                date(2022, 1, 31),
                date(2022, 2, 28),
                date(2022, 3, 31),
                date(2022, 4, 30),
            ),
        ),
        (
            (date(2022, 1, 1), date(2022, 3, 31)),
            (
                date(2022, 1, 1),
                date(2022, 2, 1),
                date(2022, 3, 1),
            ),
        ),
        (
            (date(2022, 1, 31), date(2022, 4, 1)),
            (
                date(2022, 1, 31),
                date(2022, 2, 28),
                date(2022, 3, 31),
            ),
        ),
        (
            (date(2022, 4, 1), date(2022, 1, 31)),
            (
                date(2022, 1, 31),
                date(2022, 2, 28),
                date(2022, 3, 31),
            ),
        ),
        (
            (date(2022, 1, 1), date(2022, 3, 31)),
            (
                date(2022, 1, 1),
                date(2022, 2, 1),
                date(2022, 3, 1),
            ),
        ),
        (
            (date(2022, 1, 31), date(2022, 3, 31)),
            (
                date(2022, 1, 31),
                date(2022, 2, 28),
                date(2022, 3, 31),
            ),
        ),
        ((date(2022, 1, 1), date(2022, 1, 1)), (date(2022, 1, 1),)),
    ],
)
def test_monthrange(args, expected):
    start, end = args

    output = time.monthrange(start, end)
    assert isinstance(output, types.GeneratorType)

    actual = tuple(output)
    assert actual == expected, "including start and end dates fails"

    actual = tuple(time.monthrange(start, end, include_start=False))
    assert actual == expected[1:], "excluding start date fails"

    actual = tuple(time.monthrange(start, end, include_end=False))
    assert actual == expected[:-1], "excluding end date fails"

    actual = tuple(time.monthrange(start, end, False, False))
    assert actual == expected[1:-1], "excluding start and end dates fails"


def test_mrange():
    d1 = date(2022, 1, 1)

    actual = toolz.pipe(time.mrange(d1, True), toolz.curried.take(3), list)
    expected = [date(2022, 1, 1), date(2022, 2, 1), date(2022, 3, 1)]
    assert actual == expected, "forward generation fails"

    actual = toolz.pipe(time.mrange(d1, False), toolz.curried.take(3), list)
    expected = [date(2022, 1, 1), date(2021, 12, 1), date(2021, 11, 1)]
    assert actual == expected, "backward generation fails"

    d2 = date(2022, 1, 31)

    actual = toolz.pipe(time.mrange(d2, True), toolz.curried.take(3), list)
    expected = [date(2022, 1, 31), date(2022, 2, 28), date(2022, 3, 31)]
    assert actual == expected, "forward generation fails"

    actual = toolz.pipe(time.mrange(d2, False), toolz.curried.take(3), list)
    expected = [date(2022, 1, 31), date(2021, 12, 31), date(2021, 11, 30)]
    assert actual == expected, "backward generation fails"

    d3 = date(2020, 1, 31)

    actual = toolz.pipe(time.mrange(d3, True), toolz.curried.take(3), list)
    expected = [date(2020, 1, 31), date(2020, 2, 29), date(2020, 3, 31)]
    assert actual == expected, "forward generation fails"

    d4 = date(2020, 1, 15)

    actual = toolz.pipe(time.mrange(d4, True), toolz.curried.take(3), list)
    expected = [date(2020, 1, 15), date(2020, 2, 15), date(2020, 3, 15)]
    assert actual == expected, "forward generation fails"


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
