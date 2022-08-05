import calendar
import itertools
import operator
from datetime import date, datetime, timedelta
from math import isclose

import toolz
from dateutil.relativedelta import relativedelta

from bumbag.core import op
from bumbag.math import irange


def to_date(string_to_cast):
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
    >>> to_date("2022-01-01")
    datetime.date(2022, 1, 1)
    """
    return datetime.strptime(string_to_cast, "%Y-%m-%d").date()


def to_str(date_to_cast):
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
    >>> from datetime import date
    >>> to_str(date(2022, 1, 1))
    '2022-01-01'
    """
    return date_to_cast.isoformat()


def last_date_of_month(year, month):
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
    >>> last_date_of_month(2022, 1)
    datetime.date(2022, 1, 31)
    """
    _, number_days_in_month = calendar.monthrange(year, month)
    return date(year, month, number_days_in_month)


def days_between_dates(date1, date2, include_last_date=False):
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
    >>> from datetime import date
    >>> days_between_dates(date(2022, 8, 1), date(2022, 8, 1))
    0
    >>> days_between_dates(date(2022, 8, 1), date(2022, 8, 1), True)
    1

    >>> days_between_dates(date(2022, 8, 1), date(2022, 8, 7))
    6
    >>> days_between_dates(date(2022, 8, 1), date(2022, 8, 7), True)
    7
    """
    start, end = sorted([date1, date2])
    return (end - start).days + 1 if include_last_date else (end - start).days


def daterange(start, end, include_start=True, include_end=True):
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
    >>> from datetime import date
    >>> from toolz.curried import map, pipe
    >>> from bumbag.time import to_str
    >>> d1 = date(2022, 1, 1)
    >>> d2 = date(2022, 1, 3)

    >>> pipe(daterange(d1, d2), map(to_str), list)
    ['2022-01-01', '2022-01-02', '2022-01-03']

    >>> pipe(daterange(d1, d2, False, True), map(to_str), list)
    ['2022-01-02', '2022-01-03']

    >>> pipe(daterange(d1, d2, True, False), map(to_str), list)
    ['2022-01-01', '2022-01-02']

    >>> pipe(daterange(d1, d2, False, False), map(to_str), list)
    ['2022-01-02']

    >>> pipe(daterange(date(2022, 1, 1), date(2022, 1, 1)), list)
    [datetime.date(2022, 1, 1)]

    >>> pipe(daterange(date(2022, 1, 1), date(2022, 1, 1), False), list)
    []

    >>> pipe(daterange(d2, d1), map(to_str), list)
    ['2022-01-01', '2022-01-02', '2022-01-03']
    """
    start, end = sorted([start, end])
    start = start if include_start else start + timedelta(1)
    end = end if include_end else end - timedelta(1)
    return itertools.takewhile(lambda d: d <= end, drange(start))


def drange(start, forward=True):
    """Generate an 'infinite' sequence of consecutive dates.

    Parameters
    ----------
    start : datetime.date
        Start of the sequence.
    forward : bool, default=True
        Specify if dates should be generated in a forward or backward manner.

    Yields
    ------
    datetime.date
        A generator of the date sequence.

    See Also
    --------
    bumbag.math.irange : Generate an 'infinite' number sequence.

    Examples
    --------
    >>> from datetime import date
    >>> from toolz.curried import pipe, take, map
    >>> from bumbag.time import to_str
    >>> d1 = date(2022, 1, 1)

    >>> pipe(drange(d1), map(to_str), take(3), list)
    ['2022-01-01', '2022-01-02', '2022-01-03']

    >>> pipe(drange(d1, False), map(to_str), take(3), list)
    ['2022-01-01', '2021-12-31', '2021-12-30']
    """
    successor = op(operator.add if forward else operator.sub, y=timedelta(1))
    return toolz.iterate(successor, start)


def datedelta(reference, days):
    """Compute date relative to reference date.

    The reference date and relative date are the inclusive endpoints of the
    corresponding, consecutive date sequence. As a result, the reference date
    and relative date can, for example, directly be used in a BETWEEN statement
    of a SQL query.

    Parameters
    ----------
    reference : datetime.date
        The reference date.
    days : int
        Size of the delta expressed in number of days:
         - If ``days == 0``, returns the reference date.
         - If ``days > 0``, returns the date ahead w.r.t. the reference date.
         - If ``days < 0``, returns the date ago w.r.t. the reference date.
        The value of ``days`` equals the length of the corrsponding sequence of
        consecutive dates with inclusive endpoints.

    Returns
    -------
    datetime.date
        Relative date.

    Examples
    --------
    >>> from datetime import date
    >>> datedelta(date(2022, 1, 1), 0)
    datetime.date(2022, 1, 1)

    >>> datedelta(date(2022, 1, 1), 3)
    datetime.date(2022, 1, 3)

    >>> datedelta(date(2022, 1, 1), -3)
    datetime.date(2021, 12, 30)
    """
    relative_date = reference + timedelta(days=days)
    return (
        relative_date
        if days == 0
        else relative_date - timedelta(days=1)
        if days > 0
        else relative_date + timedelta(days=1)
    )


def months_between_dates(date1, date2, include_last_date=False):
    """Compute the number of months between two dates.

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
        Number of months.

    Examples
    --------
    >>> from datetime import date
    >>> months_between_dates(date(2022, 1, 1), date(2022, 1, 1))
    0
    >>> months_between_dates(date(2022, 1, 1), date(2022, 1, 1), True)
    1

    >>> months_between_dates(date(2022, 1, 1), date(2022, 8, 31))
    7
    >>> months_between_dates(date(2022, 1, 1), date(2022, 8, 1), True)
    8
    """
    start, end = sorted([date1, date2])
    difference = relativedelta(end, start)
    n_months = difference.months + 12 * difference.years
    return n_months + 1 if include_last_date else n_months


def monthrange(start, end, include_start=True, include_end=True):
    """Generate a sequence of consecutive months between two dates.

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
        A generator of the month sequence.

    Notes
    -----
    - If ``start == end``, generating one value (with default settings).
    - If ``start > end``, swapping values.

    Examples
    --------
    >>> from datetime import date
    >>> from toolz.curried import map, pipe
    >>> from bumbag.time import to_str
    >>> d1 = date(2022, 1, 1)
    >>> d2 = date(2022, 4, 30)

    >>> pipe(monthrange(d1, d2), map(to_str), list)
    ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']

    >>> pipe(monthrange(d1, d2, False, True), map(to_str), list)
    ['2022-02-01', '2022-03-01', '2022-04-01']

    >>> pipe(monthrange(d1, d2, True, False), map(to_str), list)
    ['2022-01-01', '2022-02-01', '2022-03-01']

    >>> pipe(monthrange(d1, d2, False, False), map(to_str), list)
    ['2022-02-01', '2022-03-01']

    >>> pipe(monthrange(d1, d1), list)
    [datetime.date(2022, 1, 1)]

    >>> pipe(monthrange(d1, d1, False), list)
    []

    >>> pipe(monthrange(d2, d1), map(to_str), list)
    ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']

    >>> d1 = date(2022, 1, 31)
    >>> d2 = date(2022, 4, 30)
    >>> pipe(monthrange(d1, d2), map(to_str), list)
    ['2022-01-31', '2022-02-28', '2022-03-31', '2022-04-30']
    """
    start, end = sorted([start, end])
    n_months = months_between_dates(start, end, include_last_date=True)
    month_sequence = (start + relativedelta(months=i) for i in range(n_months))

    if not include_end:
        month_sequence = toolz.take(n_months - 1, month_sequence)

    if not include_start:
        month_sequence = toolz.drop(1, month_sequence)

    return month_sequence


def mrange(start, forward=True):
    """Generate an 'infinite' sequence of consecutive months.

    Parameters
    ----------
    start : datetime.date
        Start of the sequence.
    forward : bool, default=True
        Specify if months should be generated in a forward or backward manner.

    Yields
    ------
    datetime.date
        A generator of the month sequence.

    See Also
    --------
    bumbag.math.irange : A generator of consecutive integers.

    Examples
    --------
    >>> from datetime import date
    >>> from toolz.curried import map, pipe, take
    >>> from bumbag.time import to_str

    >>> pipe(mrange(date(2022, 1, 1)), map(to_str), take(4), list)
    ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01']

    >>> pipe(mrange(date(2022, 1, 1), False), map(to_str), take(4), list)
    ['2022-01-01', '2021-12-01', '2021-11-01', '2021-10-01']

    >>> pipe(mrange(date(2022, 1, 31)), map(to_str), take(4), list)
    ['2022-01-31', '2022-02-28', '2022-03-31', '2022-04-30']

    >>> pipe(mrange(date(2022, 1, 31), False), map(to_str), take(4), list)
    ['2022-01-31', '2021-12-31', '2021-11-30', '2021-10-31']
    """
    for i in irange(0):
        yield (
            start + relativedelta(months=i)
            if forward
            else start - relativedelta(months=i)
        )


def humantime(seconds):
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
    >>> humantime(1)
    '1 second'

    >>> humantime(2)
    '2 seconds'

    >>> humantime(60)
    '1 minute'

    >>> humantime(120)
    '2 minutes'

    >>> humantime(60 * 60 * 24 + 123456)
    '2 days, 10 hours, 17 minutes'
    """
    if seconds < 0:
        raise ValueError(f"{seconds=} - must be a non-negative number")

    if isclose(seconds, 0):
        return "0 seconds"

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    def multiplier(time_with_unit: str) -> str:
        time_without_unit = float(time_with_unit.split(" ")[0])
        return (
            time_with_unit
            if isclose(time_without_unit, 1)
            else f"{time_with_unit}s"
        )

    result = []
    if days:
        result.append(multiplier(f"{int(days)} day"))

    if hours:
        result.append(multiplier(f"{int(hours)} hour"))

    if minutes:
        result.append(multiplier(f"{int(minutes)} minute"))

    if seconds and minutes < 2:
        if isclose(seconds, int(seconds)):
            result.append(multiplier(f"{int(seconds)} second"))
        else:
            result.append(f"{seconds:0.6f} seconds")

    return ", ".join(result)
