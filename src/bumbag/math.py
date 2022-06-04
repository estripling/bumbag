import operator

import toolz

from bumbag import core


def iseq(start=1):
    """Generate a sequence of consecutive integers.

    Parameters
    ----------
    start : int, default=1
        Start of the sequence.

    Yields
    ------
    int
        A generator of consecutive integers.

    Examples
    --------
    >>> from toolz import take
    >>> list(take(11, iseq(-1)))
    [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> list(take(5, iseq()))
    [1, 2, 3, 4, 5]
    """
    add1 = core.op(operator.add, 1)
    return toolz.iterate(add1, start)


def iseq_even(start=1):
    """Generate a sequence of consecutive even integers.

    Parameters
    ----------
    start : int, default=1
        Start of the sequence.

    Yields
    ------
    int
        A generator of consecutive even integers.

    Examples
    --------
    >>> from toolz import take
    >>> list(take(11, iseq_even(-1)))
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    >>> list(take(5, iseq_even()))
    [2, 4, 6, 8, 10]
    """
    return toolz.filter(iseven, iseq(start))


def iseq_odd(start=1):
    """Generate a sequence of consecutive odd integers.

    Parameters
    ----------
    start : int, default=1
        Start of the sequence.

    Yields
    ------
    int
        A generator of consecutive odd integers.

    Examples
    --------
    >>> from toolz import take
    >>> list(take(11, iseq_odd(-1)))
    [-1, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    >>> list(take(5, iseq_odd()))
    [1, 3, 5, 7, 9]
    """
    return toolz.filter(isodd, iseq(start))


def iseven(number):
    """Check if number is even.

    Parameters
    ----------
    number : int
        Number to check.

    Returns
    -------
    bool
        Is number even.

    Examples
    --------
    >>> iseven(2)
    True
    >>> iseven(3)
    False
    """
    return number % 2 == 0


def isodd(number):
    """Check if number is odd.

    Parameters
    ----------
    number : int
        Number to check.

    Returns
    -------
    bool
        Is number odd.

    Examples
    --------
    >>> isodd(2)
    False
    >>> isodd(3)
    True
    """
    return toolz.complement(iseven)(number)
