import calendar
from datetime import date


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
