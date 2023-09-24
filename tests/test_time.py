import re
import time
from datetime import date, datetime, timedelta

import pytest
from toolz import curried

import bumbag


class TestStopwatch:
    def test_context_manager__default_call(
        self,
        slumber,
        regex_default_message,
        capsys,
    ):
        with bumbag.stopwatch():
            slumber()

        actual = capsys.readouterr().out
        expected = regex_default_message
        assert re.search(expected, actual) is not None

    def test_context_manager__instance(self, slumber, regex_default_message):
        with bumbag.stopwatch() as sw:
            slumber()

        actual = str(sw)
        expected = regex_default_message
        assert re.search(expected, actual) is not None

    @pytest.mark.parametrize("label", [None, "lbl", 1, True, 0.0, set(), [2]])
    def test_context_manager__label(
        self,
        slumber,
        regex_default_message,
        label,
    ):
        if label is not None and not isinstance(label, (str, int)):
            with pytest.raises(
                TypeError,
                match=r"label=.* - must be a string, integer, or NoneType",
            ):
                with bumbag.stopwatch(label):
                    slumber()

        else:

            with bumbag.stopwatch(label) as sw:
                slumber()

            actual = str(sw)
            expected = (
                regex_default_message
                if label is None
                else regex_default_message.replace("$", f" - {label}$")
            )
            assert re.search(expected, actual) is not None
            assert sw.label is None if label is None else sw.label == label

            with pytest.raises(AttributeError, match=r"can't set attribute"):
                sw.label = label

            with pytest.raises(
                TypeError,
                match=r"got some positional-only arguments passed as keyword arguments",
            ):
                with bumbag.stopwatch(label=label) as sw:
                    slumber()

    @pytest.mark.parametrize("flush", [True, False, None, 0, 1.0, set(), [2]])
    def test_context_manager__flush(self, slumber, regex_default_message, flush):
        if not isinstance(flush, bool):
            with pytest.raises(TypeError, match=r"flush=.* - must be bool"):
                with bumbag.stopwatch(flush=flush):
                    slumber()

        else:

            with bumbag.stopwatch(flush=flush) as sw:
                slumber()

            actual = str(sw)
            expected = regex_default_message
            assert re.search(expected, actual) is not None
            assert sw.flush == flush

            with pytest.raises(AttributeError, match=r"can't set attribute"):
                sw.flush = flush

    @pytest.mark.parametrize(
        "case,fmt",
        [
            (1, None),
            (2, "%Y-%m-%d %H:%M:%S"),
            (3, "%H:%M:%S"),
            (4, "%A, %d %B %Y %H:%M:%S"),
        ],
    )
    def test_context_manager__fmt(
        self,
        slumber,
        regex_default_message,
        case,
        fmt,
        default_fmt="%Y-%m-%d %H:%M:%S",
    ):
        with bumbag.stopwatch(fmt=fmt) as sw:
            slumber()

        actual = str(sw)
        expected = (
            regex_default_message
            if case in (1, 2)
            else self.create_regex_for_message(r"\d{2}:\d{2}:\d{2}")
            if case == 3
            else self.create_regex_for_message(
                r"\w+, \d{2} \w+ \d{4} \d{2}:\d{2}:\d{2}"
            )
            if case == 4
            else None
        )
        assert re.search(expected, actual) is not None
        assert sw.fmt == default_fmt if fmt is None else sw.fmt == fmt

        # change timestamp format but not data
        sw.fmt = default_fmt

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.start_time = datetime.now()

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.stop_time = datetime.now()

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.elapsed_time = timedelta(days=42)

        actual = str(sw)
        expected = regex_default_message
        assert re.search(expected, actual) is not None

    @pytest.mark.parametrize("label", [None, "lbl"])
    @pytest.mark.parametrize("flush", [True, False])
    @pytest.mark.parametrize(
        "case,fmt", [(1, None), (2, "%Y-%m-%d %H:%M:%S"), (3, "%H:%M:%S")]
    )
    def test_context_manager__many_param(
        self,
        slumber,
        regex_default_message,
        label,
        flush,
        case,
        fmt,
        default_fmt="%Y-%m-%d %H:%M:%S",
    ):
        with bumbag.stopwatch(label, flush=flush, fmt=fmt) as sw:
            slumber()

        actual = str(sw)
        expected_message = (
            regex_default_message
            if case in (1, 2)
            else self.create_regex_for_message(r"\d{2}:\d{2}:\d{2}")
            if case == 3
            else None
        )
        expected = (
            expected_message
            if label is None
            else expected_message.replace("$", f" - {label}$")
        )
        assert re.search(expected, actual) is not None
        assert sw.label == label
        assert sw.flush == flush
        assert sw.fmt == default_fmt if fmt is None else sw.fmt == fmt

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.label = label

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.flush = flush

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.start_time = datetime.now()

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.stop_time = datetime.now()

        with pytest.raises(AttributeError, match=r"can't set attribute"):
            sw.elapsed_time = timedelta(days=42)

    def test_decorator__default_call(self, slumber, regex_default_message, capsys):
        @bumbag.stopwatch()
        def func():
            slumber()

        func()

        actual = capsys.readouterr().out
        expected = regex_default_message.replace("$", f" - {func.__name__}$")
        assert re.search(expected, actual) is not None

    def test_decorator__label(
        self,
        slumber,
        regex_default_message,
        capsys,
        label="lbl",
    ):
        @bumbag.stopwatch(label)
        def func():
            slumber()

        func()

        actual = capsys.readouterr().out
        expected = regex_default_message.replace("$", f" - {label}$")
        assert re.search(expected, actual) is not None

    @pytest.mark.parametrize("flush", [True, False])
    def test_decorator__flush(self, slumber, regex_default_message, flush, capsys):
        @bumbag.stopwatch(flush=flush)
        def func():
            slumber()

        func()

        actual = capsys.readouterr().out
        expected = regex_default_message.replace("$", f" - {func.__name__}$")
        assert re.search(expected, actual) is not None

    @pytest.mark.parametrize(
        "case,fmt",
        [
            (1, None),
            (2, "%Y-%m-%d %H:%M:%S"),
            (3, "%H:%M:%S"),
            (4, "%A, %d %B %Y %H:%M:%S"),
        ],
    )
    def test_decorator__fmt(
        self,
        slumber,
        regex_default_message,
        case,
        fmt,
        capsys,
    ):
        @bumbag.stopwatch(fmt=fmt)
        def func():
            slumber()

        func()

        actual = capsys.readouterr().out
        expected_message = (
            regex_default_message
            if case in [1, 2]
            else self.create_regex_for_message(r"\d{2}:\d{2}:\d{2}")
            if case == 3
            else self.create_regex_for_message(
                r"\w+, \d{2} \w+ \d{4} \d{2}:\d{2}:\d{2}"
            )
            if case == 4
            else None
        )
        expected = expected_message.replace("$", f" - {func.__name__}$")
        assert re.search(expected, actual) is not None

    @pytest.mark.parametrize("label", [None, "lbl"])
    @pytest.mark.parametrize("flush", [True, False])
    @pytest.mark.parametrize(
        "case,fmt", [(1, None), (2, "%Y-%m-%d %H:%M:%S"), (3, "%H:%M:%S")]
    )
    def test_decorator__many_param(
        self,
        slumber,
        regex_default_message,
        label,
        flush,
        case,
        fmt,
        capsys,
    ):
        @bumbag.stopwatch(label, fmt=fmt, flush=flush)
        def func():
            slumber()

        func()

        actual = capsys.readouterr().out
        expected_message = (
            regex_default_message
            if case in (1, 2)
            else self.create_regex_for_message(r"\d{2}:\d{2}:\d{2}")
            if case == 3
            else None
        )
        expected = (
            expected_message.replace("$", f" - {func.__name__}$")
            if label is None
            else expected_message.replace("$", f" - {label}$")
        )
        assert re.search(expected, actual) is not None

    @pytest.fixture(scope="class")
    def slumber(self):
        def _():
            time.sleep(0.01)

        return _

    @pytest.fixture(scope="class")
    def regex_default_message(self, regex_default_fmt):
        """Regex: default output message."""
        return self.create_regex_for_message(regex_default_fmt)

    @pytest.fixture(scope="class")
    def regex_default_fmt(self):
        """Regex: default timestamp format."""
        return r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

    @staticmethod
    def create_regex_for_message(regex_fmt):
        return rf"^{regex_fmt} -> {regex_fmt} = 0\.01(\d*)?s$"


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


@pytest.mark.parametrize(
    "arg, expected",
    [
        (date(2022, 8, 1), "Mon"),
        (date(2022, 8, 2), "Tue"),
        (date(2022, 8, 3), "Wed"),
        (date(2022, 8, 4), "Thu"),
        (date(2022, 8, 5), "Fri"),
        (date(2022, 8, 6), "Sat"),
        (date(2022, 8, 7), "Sun"),
    ],
)
def test_weekday(arg, expected):
    date_to_name = arg
    actual = bumbag.weekday(date_to_name)
    assert actual == expected
