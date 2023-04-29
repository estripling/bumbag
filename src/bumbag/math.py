import toolz

__all__ = (
    "collatz",
    "fibonacci",
    "isdivisibleby",
    "iseven",
    "isodd",
)


def collatz(number, /):
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
    >>> import bumbag
    >>> import toolz
    >>> list(bumbag.collatz(12))
    [12, 6, 3, 10, 5, 16, 8, 4, 2, 1]
    >>> toolz.count(bumbag.collatz(12))
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
    >>> import bumbag
    >>> import toolz
    >>> list(toolz.take(10, bumbag.fibonacci()))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    lag1, lag2 = 1, 0
    yield lag2
    yield lag1

    while True:
        lag0 = lag1 + lag2
        yield lag0
        lag1, lag2 = lag0, lag1


@toolz.curry
def isdivisibleby(x, number, /):
    """Check if number is evenly divisible by x.

    Parameters
    ----------
    x : int
        Specify the divisor.
    number : int
        Specify the number to check.

    Returns
    -------
    bool
        ``True`` if number is evenly divisible by x else ``False``.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> import bumbag
    >>> bumbag.isdivisibleby(2, 10)
    True

    >>> bumbag.isdivisibleby(2, 9)
    False

    >>> iseven = bumbag.isdivisibleby(2)
    >>> iseven(10)
    True
    """
    return number % x == 0


def iseven(number, /):
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
    >>> import bumbag
    >>> bumbag.iseven(2)
    True

    >>> bumbag.iseven(3)
    False
    """
    return isdivisibleby(2)(number)


def isodd(number, /):
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
    >>> import bumbag
    >>> bumbag.isodd(2)
    False

    >>> bumbag.isodd(3)
    True
    """
    return toolz.complement(iseven)(number)
