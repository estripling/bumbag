import operator

import toolz

from bumbag import core


def collatz(number):
    """Generate the Collatz sequence for a positive integer.

    The famous 3n + 1 conjecture. Given a positive integer :math:`n > 0`,
    the next term in the Collatz sequence is half of :math:`n`
    if :math:`n` is even; otherwise, if :math:`n` is odd,
    the next term is 3 times :math:`n` plus 1.
    Symbolically,

    .. math::

        f(n) =
        \\begin{cases}
            \\frac{n}{2} & \\text{ if } n \\equiv 0 \\text{ (mod 2) } \\\\[6pt]
            3n + 1 & \\text{ if } n \\equiv 1 \\text{ (mod 2) }
        \\end{cases}

    The Collatz conjecture is that the sequence always reaches 1
    for any positive integer.

    Parameters
    ----------
    number : int
        A positive integer seeding the Collatz sequence.

    Yields
    ------
    int
        A generator of Collatz numbers that breaks when 1 is reached.

    Raises
    ------
    ValueError
        If ``number`` is not a positive integer.

    References
    ----------
    .. [1] "Collatz", The On-Line Encyclopedia of Integer Sequences®,
           https://oeis.org/A006370

    .. [2] "Collatz conjecture", Wikipedia,
           https://en.wikipedia.org/wiki/Collatz_conjecture

    Examples
    --------
    >>> from toolz import count
    >>> list(collatz(12))
    [12, 6, 3, 10, 5, 16, 8, 4, 2, 1]
    >>> count(collatz(12))
    10
    """
    if not isinstance(number, int) or number < 1:
        raise ValueError(f"{number=} - must be a positive integer")

    while True:
        yield number

        if number == 1:
            break

        # update
        number = number // 2 if iseven(number) else 3 * number + 1


def fibonacci():
    """Generate the Fibonacci sequence.

    Yields
    ------
    int
        A generator of consecutive Fibonacci numbers.

    References
    ----------
    .. [1] "Fibonacci numbers", The On-Line Encyclopedia of Integer Sequences®,
           https://oeis.org/A000045
    .. [2] "Fibonacci number", Wikipedia,
           https://en.wikipedia.org/wiki/Fibonacci_number

    Examples
    --------
    >>> from toolz import take
    >>> list(take(10, fibonacci()))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    lag1, lag2 = 1, 0
    yield lag2
    yield lag1

    while True:
        lag0 = lag1 + lag2
        yield lag0
        lag1, lag2 = lag0, lag1


def irange(start, step=1):
    """Generate an 'infinite' sequence of consecutive, equidistance numbers.

    Parameters
    ----------
    start : int, float
        Start of the sequence.
    step : int, float, default=1
        Step size to use.

    Yields
    ------
    int
        A generator of the number sequence.

    Raises
    ------
    TypeError
        If ``start`` and ``step`` are not ``int`` or ``float``.
    ValueError
        If ``step`` is not a positive number.

    See Also
    --------
    bumbag.time.drange : Generate an 'infinite' date sequence.

    Examples
    --------
    >>> import itertools
    >>> import math
    >>> from toolz.curried import curry, filter, map, pipe, take
    >>> from bumbag.core import sig
    >>> from bumbag.math import iseven, isodd, irange
    >>> takewhile = curry(itertools.takewhile)
    >>> power = curry(math.pow)
    >>> power2 = power(2)
    >>> power10 = power(10)

    >>> pipe(irange(1), take(5), list)
    [1, 2, 3, 4, 5]

    >>> pipe(irange(-2), takewhile(lambda x: x <= 2), list)
    [-2, -1, 0, 1, 2]

    >>> pipe(irange(0, step=0.1), map(sig), takewhile(lambda x: x <= 1), list)
    [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    >>> pipe(irange(-5), takewhile(lambda x: x <= 5), map(power2), list)
    [0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]

    >>> pipe(irange(-5), takewhile(lambda x: x <= 4), map(power10), list)
    [1e-05, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]

    >>> pipe(irange(0), filter(iseven), take(5), list)
    [0, 2, 4, 6, 8]

    >>> pipe(irange(0), filter(isodd), take(5), list)
    [1, 3, 5, 7, 9]

    >>> pipe(irange(0, step=4), map(lambda x: -x), take(5), list)
    [0, -4, -8, -12, -16]
    """
    if not isinstance(start, (int, float)):
        raise TypeError(f"{type(start)=} - must be 'int' or 'float'")

    if not isinstance(step, (int, float)):
        raise TypeError(f"{type(step)=} - must be 'int' or 'float'")

    if step <= 0:
        raise ValueError(f"{step=} - must be a positive number")

    successor = core.op(operator.add, y=step)
    return toolz.iterate(successor, start)


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
