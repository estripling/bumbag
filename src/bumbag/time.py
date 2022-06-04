import calendar
from datetime import date, timedelta


def get_last_date_of_month(year, month):
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
    >>> get_last_date_of_month(2022, 1)
    datetime.date(2022, 1, 31)
    """
    _, number_days_in_month = calendar.monthrange(year, month)
    return date(year, month, number_days_in_month)


def is_leap_year(year):
    """Check if year is a leap year.

    Parameters
    ----------
    year : int
        Year to check.

    Returns
    -------
    bool
        Is leap year.

    Examples
    --------
    >>> is_leap_year(2000)
    True
    >>> is_leap_year(2001)
    False
    """
    return calendar.isleap(year)


def daterange(start, end, exclude_start=False, exclude_end=False):
    """Get sequence of dates.

    Parameters
    ----------
    start : datetime.date
        Start of the date sequence.
    end : datetime.date
        End of the date sequence.
    exclude_start : bool, default=False
        Specifies if the start date of the sequence should be excluded.
    exclude_end : bool, default=False
        Specifies if the end date of the sequence should be excluded.

    Yields
    ------
    datetime.date
        A generator of consecutive dates from ``start`` to ``end``.

    Examples
    --------
    >>> list(daterange(date(2022, 1, 1), date(2022, 1, 3)))
    [date(2022, 1, 1), date(2022, 1, 2), date(2022, 1, 3)]
    """
    n_days = (end - start).days + 1
    for i in range(n_days):
        if (i == 0 and exclude_start) or ((i + 1) == n_days and exclude_end):
            continue
        yield start + timedelta(i)
