import operator

import toolz

from bumbag import core


def iseq(start=0):
    """Generate a sequence of consecutive integers.

    Parameters
    ----------
    start : int, default=0
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
    """
    add1 = core.op(operator.add, 1)
    return toolz.iterate(add1, start)


def iseq_even(start=0):
    """Generate a sequence of consecutive even integers.

    Parameters
    ----------
    start : int, default=0
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
    [0, 2, 4, 6, 8]
    """
    return toolz.filter(iseven, iseq(start))


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
