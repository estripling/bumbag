import calendar
import math
from datetime import date, datetime, timedelta


def str_to_date(string):
    """Cast an ISO date string to a date object.

    Parameters
    ----------
    string : str
        ISO date string to cast.

    Returns
    -------
    datetime.date
        ISO date.

    Examples
    --------
    >>> str_to_date("2022-01-01")
    datetime.date(2022, 1, 1)
    """
    return datetime.strptime(string, "%Y-%m-%d").date()


def date_to_str(input_date):
    """Cast an ISO date object to string.

    Parameters
    ----------
    input_date : datetime.date
        ISO date object to cast.

    Returns
    -------
    str
        ISO date.

    Examples
    --------
    >>> from datetime import date
    >>> date_to_str(date(2022, 1, 1))
    '2022-01-01'
    """
    return datetime.strftime(input_date, "%Y-%m-%d")


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
    >>> # noqa E501
    >>> list(daterange(date(2022, 1, 1), date(2022, 1, 3)))
    [datetime.date(2022, 1, 1), datetime.date(2022, 1, 2), datetime.date(2022, 1, 3)]
    """
    n_days = (end - start).days + 1
    for i in range(n_days):
        if (i == 0 and exclude_start) or ((i + 1) == n_days and exclude_end):
            continue
        yield start + timedelta(i)


def humantime(seconds):
    """Convert seconds to human-readable time.

    Parameters
    ----------
    seconds : int, float
        Seconds to convert.

    Returns
    -------
    str
        Human-readable time.

    Raises
    ------
    ValueError
        If ``seconds`` is not a positive integer.

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
        raise ValueError(f"seconds={seconds} - must be a non-negative number")

    if math.isclose(seconds, 0):
        return "0 seconds"

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    def multiplier(time_with_unit: str) -> str:
        time_without_unit = float(time_with_unit.split(" ")[0])
        return (
            time_with_unit
            if math.isclose(time_without_unit, 1)
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
        if math.isclose(seconds, int(seconds)):
            result.append(multiplier(f"{int(seconds)} second"))
        else:
            result.append(f"{seconds:0.6f} seconds")

    return ", ".join(result)
