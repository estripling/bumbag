import calendar
import itertools
import math
import operator
from contextlib import ContextDecorator
from datetime import date, datetime, timedelta

import toolz
from dateutil.relativedelta import relativedelta

from bumbag import core

__all__ = (
    "datedelta",
    "daterange",
    "days_between_dates",
    "daycount",
    "humantime",
    "last_date_of_month",
    "months_between_dates",
    "stopwatch",
    "to_date",
    "to_str",
    "weekday",
)


class stopwatch(ContextDecorator):
    """Measure elapsed wall-clock time and print it to standard output.

    Parameters
    ----------
    label : None, str, int, default=None
        Optionally specify a label for easy identification.
    flush : bool, default=True
        Passed to built-in print function:
         - If ``True``, prints start time before stop time.
         - If ``False``, prints start time and stop time all at once.
    fmt : None, str, default=None
        Optionally specify a timestamp format to be used in the output message.
        If ``fmt`` is None, the following format is used: ``%Y-%m-%d %H:%M:%S``.

    Notes
    -----
    Object creation and use of an object's properties is only possible
    when ``stopwatch`` is used as a context manager (see examples).

    Examples
    --------
    >>> # as context manager
    >>> import bumbag
    >>> import time
    >>> with bumbag.stopwatch():  # doctest: +SKIP
    ...     time.sleep(0.1)
    ...
    2023-01-01 12:00:00 -> 2023-01-01 12:00:00 = 0.100691s

    >>> # as decorator
    >>> import bumbag
    >>> import time
    >>> @bumbag.stopwatch()
    ... def func():
    ...     time.sleep(0.1)
    ...
    >>> func()  # doctest: +SKIP
    2023-01-01 12:00:00 -> 2023-01-01 12:00:00 = 0.100709s - func

    >>> # stopwatch instance
    >>> import bumbag
    >>> import time
    >>> with bumbag.stopwatch("instance-example") as sw:  # doctest: +SKIP
    ...     time.sleep(0.1)
    ...
    2023-01-01 12:00:00 -> 2023-01-01 12:00:00 = 0.100647s - instance-example
    >>> sw.label  # doctest: +SKIP
    'instance-example'
    >>> sw.flush  # doctest: +SKIP
    True
    >>> sw.fmt  # doctest: +SKIP
    '%Y-%m-%d %H:%M:%S'
    >>> sw.start_time  # doctest: +SKIP
    datetime.datetime(2023, 1, 1, 12, 0, 0, 732176)
    >>> sw.stop_time  # doctest: +SKIP
    datetime.datetime(2023, 1, 1, 12, 0, 0, 832823)
    >>> sw.elapsed_time  # doctest: +SKIP
    datetime.timedelta(microseconds=100647)
    >>> sw  # doctest: +SKIP
    2023-01-01 12:00:00 -> 2023-01-01 12:00:00 = 0.100647s - instance-example
    """

    def __init__(self, label=None, /, *, flush=True, fmt=None):
        if label is not None and not isinstance(label, (str, int)):
            raise TypeError(f"{label=} - must be a string, integer, or NoneType")

        self._label = label
        self._flush = flush
        self._fmt = "%Y-%m-%d %H:%M:%S" if fmt is None else fmt
        self._start_time = None
        self._stop_time = None
        self._elapsed_time = None

    def __repr__(self):
        return (
            super().__repr__() if self.elapsed_time is None else self._output_message()
        )

    @property
    def label(self):
        """Retrieve label value.

        Returns
        -------
        NoneType or str
            Label if specified in the call else None.
            When used as a decorator and label is not specified in the call,
            label is the name of the decorated function.
        """
        return self._label

    @property
    def flush(self):
        """Retrieve flush value.

        Returns
        -------
        bool
            Value used in the built-in function when printing to standard output.
        """
        return self._flush

    @property
    def fmt(self):
        """Retrieve timestamp format.

        The timestamp format can be changed by passing a new value that is accepted
        by ``strftime``. Note that the underlying data remain unchanged.

        Returns
        -------
        str
            Format to use to convert a ``datetime`` object to a string via ``strftime``.
        """
        return self._fmt

    @fmt.setter
    def fmt(self, value):
        self._fmt = value

    @property
    def start_time(self):
        """Retrieve start time value.

        Returns
        -------
        datetime.datetime
            Timestamp of the start time.
        """
        return self._start_time

    @property
    def stop_time(self):
        """Retrieve stop time value.

        Returns
        -------
        datetime.datetime
            Timestamp of the stop time.
        """
        return self._stop_time

    @property
    def elapsed_time(self):
        """Retrieve elapsed time value.

        Returns
        -------
        datetime.timedelta
            The elapsed time between start and stop.
        """
        return self._elapsed_time

    def __call__(self, func):
        if self.label is None:
            self._label = func.__name__
        return super().__call__(func)

    def __enter__(self):
        self._start_time = datetime.now()
        if self.flush:
            print(self._message_part_1(), end="", flush=True)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._stop_time = datetime.now()
        self._elapsed_time = self.stop_time - self.start_time
        print(self._message_part_2() if self.flush else self._output_message())
        return False

    def _output_message(self):
        return self._message_part_1() + self._message_part_2()

    def _message_part_1(self):
        return self._datetime_to_str(self.start_time) + " -> "

    def _message_part_2(self):
        suffix = "" if self.label is None else f" - {self.label}"
        return (
            self._datetime_to_str(self.stop_time)
            + " = "
            + self._human_readable_elapsed_time()
            + suffix
        )

    def _human_readable_elapsed_time(self):
        if self.elapsed_time is not None:
            return humantime(self.elapsed_time.total_seconds())

    def _datetime_to_str(self, date_time):
        return date_time.strftime(self.fmt)


def datedelta(reference_date, /, *, days):
    """Compute date relative to reference date.

    The reference date and relative date are the inclusive endpoints of the
    corresponding, consecutive date sequence. As a result, the reference date
    and relative date can, for example, directly be used in a BETWEEN statement
    of a SQL query.

    Parameters
    ----------
    reference_date : datetime.date
        Specify reference date.
    days : int
        Size of the delta expressed in number of days:
         - If ``days == 0``, returns the reference date.
         - If ``days > 0``, returns the date ahead w.r.t. the reference date.
         - If ``days < 0``, returns the date ago w.r.t. the reference date.
        The value of ``days`` equals the length of the corresponding sequence of
        consecutive dates with inclusive endpoints.

    Returns
    -------
    datetime.date
        Relative date.

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> reference_date = date(2022, 1, 1)
    >>> bumbag.datedelta(reference_date, days=0)
    datetime.date(2022, 1, 1)

    >>> bumbag.datedelta(reference_date, days=3)
    datetime.date(2022, 1, 3)

    >>> bumbag.datedelta(reference_date, days=-3)
    datetime.date(2021, 12, 30)
    """
    relative_date = reference_date + timedelta(days=days)
    return (
        relative_date
        if days == 0
        else relative_date - timedelta(days=1)
        if days > 0
        else relative_date + timedelta(days=1)
    )


def daterange(start, end, /, *, include_start=True, include_end=True):
    """Generate a sequence of consecutive days between two dates.

    Parameters
    ----------
    start : datetime.date
        Start of the sequence.
    end : datetime.date
        End of the sequence.
    include_start : bool, default=True
        Specify if sequence should include start date.
    include_end : bool, default=True
        Specify if sequence should include end date.

    Yields
    ------
    datetime.date
        A generator of the date sequence.

    Notes
    -----
    - If ``start == end``, generating one value (with default settings).
    - If ``start > end``, swapping values.

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> from toolz import curried
    >>> d1 = date(2022, 1, 1)
    >>> d2 = date(2022, 1, 3)

    >>> curried.pipe(bumbag.daterange(d1, d2), curried.map(bumbag.to_str), list)
    ['2022-01-01', '2022-01-02', '2022-01-03']

    >>> curried.pipe(
    ...     bumbag.daterange(d1, d2, include_start=False, include_end=True),
    ...     curried.map(bumbag.to_str),
    ...     list,
    ... )
    ['2022-01-02', '2022-01-03']

    >>> curried.pipe(
    ...     bumbag.daterange(d1, d2, include_start=True, include_end=False),
    ...     curried.map(bumbag.to_str),
    ...     list,
    ... )
    ['2022-01-01', '2022-01-02']

    >>> curried.pipe(
    ...     bumbag.daterange(d1, d2, include_start=False, include_end=False),
    ...     curried.map(bumbag.to_str),
    ...     list,
    ... )
    ['2022-01-02']

    >>> curried.pipe(bumbag.daterange(date(2022, 1, 1), date(2022, 1, 1)), list)
    [datetime.date(2022, 1, 1)]

    >>> curried.pipe(
    ...     bumbag.daterange(date(2022, 1, 1), date(2022, 1, 1), include_start=False),
    ...     list,
    ... )
    []

    >>> curried.pipe(bumbag.daterange(d2, d1), curried.map(bumbag.to_str), list)
    ['2022-01-01', '2022-01-02', '2022-01-03']

    >>> # month sequence - first date
    >>> curried.pipe(
    ...     bumbag.daterange(date(2022, 1, 1), date(2022, 4, 30)),
    ...     curried.filter(lambda d: d.day == 1),
    ...     curried.map(bumbag.to_str),
    ...     list,
    ... )
    ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']

    >>> # month sequence - last date
    >>> curried.pipe(
    ...     bumbag.daterange(date(2022, 1, 1), date(2022, 4, 30)),
    ...     curried.filter(lambda d: d.day == 1),
    ...     curried.map(lambda d: last_date_of_month(d.year, d.month)),
    ...     curried.map(bumbag.to_str),
    ...     list,
    ... )
    ['2022-01-31', '2022-02-28', '2022-03-31', '2022-04-30']
    """
    start, end = sorted([start, end])
    start = start if include_start else start + timedelta(1)
    end = end if include_end else end - timedelta(1)
    return itertools.takewhile(lambda d: d <= end, daycount(start))


def days_between_dates(date1, date2, /, *, include_last_date=False):
    """Compute the number of days between two dates.

    Parameters
    ----------
    date1 : datetime.date
        First reference date.
    date2 : datetime.date
        Second reference date.
    include_last_date : bool, default=False
        Specify if the larger date should be included in the computation:
         - If ``False``, number of days based on date interval [date1, date2).
         - If ``True``, number of days based on date interval [date1, date2].

    Notes
    -----
    - If ``date1 > date2``, swapping values.

    Returns
    -------
    int
        Number of days.

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> bumbag.days_between_dates(date(2022, 8, 1), date(2022, 8, 1))
    0
    >>> bumbag.days_between_dates(
    ...     date(2022, 8, 1), date(2022, 8, 1), include_last_date=True
    ... )
    1

    >>> bumbag.days_between_dates(date(2022, 8, 1), date(2022, 8, 7))
    6
    >>> bumbag.days_between_dates(
    ...     date(2022, 8, 1), date(2022, 8, 7), include_last_date=True
    ... )
    7
    """
    start, end = sorted([date1, date2])
    return (end - start).days + 1 if include_last_date else (end - start).days


def daycount(start_date, /, *, forward=True):
    """Generate an in principle infinite sequence of consecutive dates.

    Parameters
    ----------
    start_date : datetime.date
        Specify the start date of the sequence.
    forward : bool, default=True
        Specify if dates should be generated in a forward or backward manner.

    Yields
    ------
    datetime.date
        A generator of the date sequence.

    See Also
    --------
    itertools.count : Generate an in principle infinite number sequence.

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> from toolz import curried
    >>> d1 = date(2022, 1, 1)

    >>> curried.pipe(
    ...     bumbag.daycount(d1), curried.map(bumbag.to_str), curried.take(3), list
    ... )
    ['2022-01-01', '2022-01-02', '2022-01-03']

    >>> curried.pipe(
    ...     bumbag.daycount(d1, forward=False),
    ...     curried.map(bumbag.to_str),
    ...     curried.take(3),
    ...     list,
    ... )
    ['2022-01-01', '2021-12-31', '2021-12-30']

    >>> curried.pipe(
    ...     bumbag.daycount(d1, forward=False),
    ...     curried.map(bumbag.to_str),
    ...     curried.take(3),
    ...     list,
    ... )
    ['2022-01-01', '2021-12-31', '2021-12-30']

    >>> # month sequence - first date
    >>> curried.pipe(
    ...     bumbag.daycount(d1),
    ...     curried.filter(lambda d: d.day == 1),
    ...     curried.map(bumbag.to_str),
    ...     curried.take(5),
    ...     list,
    ... )
    ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01']

    >>> # month sequence - last date
    >>> curried.pipe(
    ...     bumbag.daycount(d1),
    ...     curried.filter(lambda d: d.day == 1),
    ...     curried.map(lambda d: bumbag.last_date_of_month(d.year, d.month)),
    ...     curried.map(bumbag.to_str),
    ...     curried.take(5),
    ...     list,
    ... )
    ['2022-01-31', '2022-02-28', '2022-03-31', '2022-04-30', '2022-05-31']

    >>> # Monday sequence
    >>> curried.pipe(
    ...     bumbag.daycount(d1),
    ...     curried.filter(lambda d: weekday(d) == "Mon"),
    ...     curried.map(bumbag.to_str),
    ...     curried.take(5),
    ...     list,
    ... )
    ['2022-01-03', '2022-01-10', '2022-01-17', '2022-01-24', '2022-01-31']

    >>> # pick every 7th day
    >>> curried.pipe(
    ...     bumbag.daycount(d1),
    ...     curried.take_nth(7),
    ...     curried.map(bumbag.to_str),
    ...     curried.take(5),
    ...     list,
    ... )
    ['2022-01-01', '2022-01-08', '2022-01-15', '2022-01-22', '2022-01-29']
    """
    successor = core.op(operator.add if forward else operator.sub, y=timedelta(1))
    return toolz.iterate(successor, start_date)


def humantime(seconds, /):
    """Convert seconds to human-readable time.

    Parameters
    ----------
    seconds : int, float
        Seconds to convert, a non-negative number.

    Returns
    -------
    str
        Human-readable time.

    Raises
    ------
    ValueError
        If ``seconds`` is a negative number.

    Examples
    --------
    >>> import bumbag
    >>> # 1 second
    >>> bumbag.humantime(1)
    '1s'

    >>> # 1 minute
    >>> bumbag.humantime(60)
    '1m'

    >>> # 1 hour
    >>> bumbag.humantime(60 * 60)
    '1h'

    >>> # 1 day
    >>> bumbag.humantime(60 * 60 * 24)
    '1d'

    >>> bumbag.humantime(60 * 60 * 24 + 60 * 60 + 60 + 1)
    '1d 1h 1m 1s'

    >>> bumbag.humantime(3 * 60 * 60 * 24 + 2 * 60)
    '3d 2m'
    """
    if seconds < 0:
        raise ValueError(f"{seconds=} - must be a non-negative number")

    if math.isclose(seconds, 0):
        return "0s"

    if 0 < seconds < 60:
        return f"{seconds:g}s"

    minutes, seconds = divmod(int(round(seconds, 0)), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    output = []
    if days:
        output.append(f"{days}d")

    if hours:
        output.append(f"{hours}h")

    if minutes:
        output.append(f"{minutes}m")

    if seconds:
        output.append(f"{seconds}s")

    return " ".join(output)


def last_date_of_month(year, month, /):
    """Get last date of month.

    Parameters
    ----------
    year : int
        Year of date.
    month : int
        Month of date.

    Returns
    -------
    datetime.date
        Last date of month.

    Examples
    --------
    >>> import bumbag
    >>> bumbag.last_date_of_month(2022, 1)
    datetime.date(2022, 1, 31)
    """
    _, number_days_in_month = calendar.monthrange(year, month)
    return date(year, month, number_days_in_month)


def months_between_dates(date1, date2, /, *, include_last_date=False):
    """Compute the number of months between two dates.

    Parameters
    ----------
    date1 : datetime.date
        Specify the first reference date.
    date2 : datetime.date
        Specify the second reference date.
    include_last_date : bool, default=False
        Specify if the larger date should be included in the computation:
         - If ``False``, number of days based on date interval [date1, date2).
         - If ``True``, number of days based on date interval [date1, date2].

    Notes
    -----
    - If ``date1 > date2``, swapping values.

    Returns
    -------
    int
        Number of months.

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> bumbag.months_between_dates(date(2022, 1, 1), date(2022, 1, 1))
    0
    >>> bumbag.months_between_dates(
    ...     date(2022, 1, 1), date(2022, 1, 1), include_last_date=True
    ... )
    1

    >>> bumbag.months_between_dates(date(2022, 1, 1), date(2022, 8, 31))
    7
    >>> bumbag.months_between_dates(
    ...     date(2022, 1, 1), date(2022, 8, 1), include_last_date=True
    ... )
    8
    """
    start, end = sorted([date1, date2])
    difference = relativedelta(end, start)
    n_months = difference.months + 12 * difference.years
    return n_months + 1 if include_last_date else n_months


def to_date(string_to_cast, /):
    """Cast an ISO date string to a date object.

    Parameters
    ----------
    string_to_cast : str
        Date string in ISO format (YYYY-MM-DD) to cast.

    Returns
    -------
    datetime.date
        Date object.

    Examples
    --------
    >>> import bumbag
    >>> bumbag.to_date("2022-01-01")
    datetime.date(2022, 1, 1)
    """
    return datetime.strptime(string_to_cast, "%Y-%m-%d").date()


def to_str(date_to_cast, /):
    """Cast a date object to an ISO date string.

    Parameters
    ----------
    date_to_cast : datetime.date
        Date object to cast.

    Returns
    -------
    str
        Date string in ISO format (YYYY-MM-DD).

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> bumbag.to_str(date(2022, 1, 1))
    '2022-01-01'
    """
    return date_to_cast.isoformat()


def weekday(a_date, /):
    """Get name of the weekday.

    Parameters
    ----------
    a_date : datetime.date
        Specify date to extract weekday name from.

    Returns
    -------
    str
        Name of the weekday.

    Examples
    --------
    >>> import bumbag
    >>> from datetime import date
    >>> d1 = date(2022, 8, 1)
    >>> d2 = date(2022, 8, 5)
    >>> list(map(bumbag.weekday, bumbag.daterange(d1, d2)))
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

    >>> bumbag.weekday(date(2022, 8, 6))
    'Sat'

    >>> bumbag.weekday(date(2022, 8, 7))
    'Sun'
    """
    return a_date.strftime("%a")
