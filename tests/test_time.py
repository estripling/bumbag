from datetime import date

import pytest
from toolz import curried

import bumbag


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

    relative_date = bumbag.datedelta(reference_date, days=days)
    assert relative_date == expected, "relative date does not match expected"

    n_days = curried.count(bumbag.daterange(reference_date, relative_date))
    n_days_expected = 1 if days == 0 else abs(days)
    assert n_days == n_days_expected, "number of days does not match expected"


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

    actual = tuple(bumbag.daterange(start, end))
    assert actual == expected, "including start and end dates fails"

    actual = tuple(bumbag.daterange(start, end, include_start=False))
    assert actual == expected[1:], "excluding start date fails"

    actual = tuple(bumbag.daterange(start, end, include_end=False))
    assert actual == expected[:-1], "excluding end date fails"

    actual = tuple(bumbag.daterange(start, end, include_start=False, include_end=False))
    assert actual == expected[1:-1], "excluding start and end dates fails"


@pytest.mark.parametrize(
    "arg, expected",
    [
        (date(2022, 8, 1), "Monday"),
        (date(2022, 8, 2), "Tuesday"),
        (date(2022, 8, 3), "Wednesday"),
        (date(2022, 8, 4), "Thursday"),
        (date(2022, 8, 5), "Friday"),
        (date(2022, 8, 6), "Saturday"),
        (date(2022, 8, 7), "Sunday"),
    ],
)
def test_day_of_week(arg, expected):
    date_to_name = arg
    actual = bumbag.day_of_week(date_to_name)
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
    d1, d2, with_last_date = args
    actual = bumbag.days_between_dates(d1, d2, include_last_date=with_last_date)
    assert actual == expected


def test_daycount():
    d1 = date(2022, 1, 1)

    actual = curried.pipe(bumbag.daycount(d1, forward=True), curried.take(3), list)
    expected = [date(2022, 1, 1), date(2022, 1, 2), date(2022, 1, 3)]
    assert actual == expected, "forward generation fails"

    actual = curried.pipe(bumbag.daycount(d1, forward=False), curried.take(3), list)
    expected = [date(2022, 1, 1), date(2021, 12, 31), date(2021, 12, 30)]
    assert actual == expected, "backward generation fails"


@pytest.mark.parametrize(
    "arg, expected",
    [
        (-2.0, None),
        (-1, None),
        (0, "0s"),
        (1, "1s"),
        (59, "59s"),
        (59.0, "59s"),
        (60, "1m"),
        (60.1, "1m"),
        (61, "1m 1s"),
        (61.1, "1m 1s"),
        (120, "2m"),
        (120.1, "2m"),
        (60 * 60, "1h"),
        (60 * 60 + 1, "1h 1s"),
        (60 * 60 * 24, "1d"),
        (60 * 60 * 24 + 1, "1d 1s"),
        (110.0, "1m 50s"),
        (0.4142135623730951, "0.414214s"),
        (0.5, "0.5s"),
        (1.4142135623730951, "1.41421s"),
        (1.5, "1.5s"),
        (2.4142135623730951, "2.41421s"),
        (59.4142135623730951, "59.4142s"),
        (60.4142135623730951, "1m"),
        (60.5142135623730951, "1m 1s"),
        (60 * 60 * 24 + 123456, "2d 10h 17m 36s"),
    ],
)
def test_humantime(arg, expected):
    if arg < 0:
        with pytest.raises(ValueError):
            bumbag.humantime(arg)
    else:
        actual = bumbag.humantime(arg)
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
    actual = bumbag.last_date_of_month(arg.year, arg.month)
    assert actual == expected


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
    d1, d2, with_last_date = args
    actual = bumbag.months_between_dates(d1, d2, include_last_date=with_last_date)
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        ("2022-01-01", date(2022, 1, 1)),
        ("2022-01-31", date(2022, 1, 31)),
    ],
)
def test_to_date(arg, expected):
    actual = bumbag.to_date(arg)
    assert actual == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        (date(2022, 1, 1), "2022-01-01"),
        (date(2022, 1, 31), "2022-01-31"),
    ],
)
def test_to_str(arg, expected):
    actual = bumbag.to_str(arg)
    assert actual == expected
