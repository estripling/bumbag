import calendar
import itertools
import math
import operator
from contextlib import contextmanager
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


@contextmanager
def stopwatch():
    """Measure elapsed wall-clock time.

    Returns
    -------
    NoneType
        Function has no return value.
        Measurement is printed to standard output.

    Examples
    --------
    >>> # as context manager
    >>> import bumbag
    >>> import time
    >>> with bumbag.stopwatch():  # doctest: +SKIP
    ...     time.sleep(0.1)
    ...
    2023-09-17 14:50:32 -> 2023-09-17 14:50:32 = 0.100691s

    >>> # as decorator
    >>> import bumbag
    >>> import time
    >>> @bumbag.stopwatch()
    ... def my_function():
    ...     time.sleep(0.1)
    ...
    >>> my_function()  # doctest: +SKIP
    2023-09-17 14:57:00 -> 2023-09-17 14:57:00 = 0.100709s
    """
    t0 = datetime.now()
    yield
    t1 = datetime.now()
    elapsed = t1 - t0
    fmt = "%Y-%m-%d %H:%M:%S"
    timestamps = f"{t0.strftime(fmt)} -> {t1.strftime(fmt)}"
    print(f"{timestamps} = {humantime(elapsed.total_seconds())}")


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
