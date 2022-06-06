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

    See Also
    --------
    bumbag.time.dseq : A generator of consecutive dates.

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


def fibonacci():
    """Generate the Fibonacci sequence.

    Yields
    ------
    int
        A generator of consecutive Fibonacci numbers.

    References
    ----------
    .. [1] "Fibonacci number", Wikipedia,
           https://en.wikipedia.org/wiki/Fibonacci_number

    Examples
    --------
    >>> from toolz import take
    >>> list(take(10, fibonacci()))
    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    n1, n2 = 0, 1
    nth = n1 + n2
    while True:
        yield nth
        # update
        nth = n1 + n2
        n1, n2 = n2, nth


def collatz(number):
    """Generate the Collatz sequence for a positive integer.

    The famous 3n + 1 conjecture. Given a positive integer as starting term,
    the next term in the Collatz sequence is half of the previous term
    if the previous term is even; otherwise, the next term is 3 times the
    previous term plus 1 if the previous term is odd. The conjecture is that
    the Collatz sequence always reaches 1 for any positive integer as
    starting term.

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
    .. [1] "Collatz conjecture", Wikipedia,
           https://en.wikipedia.org/wiki/Collatz_conjecture

    Examples
    --------
    >>> list(collatz(12))
    [12, 6, 3, 10, 5, 16, 8, 4, 2, 1]
    >>> from toolz import count
    >>> count(collatz(12))
    10
    """
    if not isinstance(number, int) or number < 1:
        raise ValueError(f"number={number} - must be a non-negative number")

    while True:
        yield number

        if number == 1:
            break

        # update
        number = number // 2 if iseven(number) else 3 * number + 1


def two_set_summary(x, y, show=3):
    """Summary of two sets.

    Parameters
    ----------
    x : set
        Left set.
    y : set
        Right set.
    show : int, default=3
        Specific how many elements per set to show in report.

    Returns
    -------
    dict of sets

    References
    ----------
    .. [1] "Basic set operations", Wikipedia,
           https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations
    .. [2] "Jaccard index", Wikipedia,
           https://en.wikipedia.org/wiki/Jaccard_index
    .. [3] "Overlap coefficient", Wikipedia,
           https://en.wikipedia.org/wiki/Overlap_coefficient

    Examples
    --------
    >>> x = {"a", "c", "b", "g", "h"}
    >>> y = {"c", "d", "e", "f", "g"}
    >>> summary = two_set_summary(x, y)
    >>> isinstance(summary, dict)
    True
    >>> summary["x"] == x
    True
    >>> summary["y"] == y
    True
    >>> summary["x | y"] == x.union(y)
    True
    >>> summary["x & y"] == x.intersection(y)
    True
    >>> summary["x - y"] == x.difference(y)
    True
    >>> summary["y - x"] == y.difference(x)
    True
    >>> summary["x ^ y"] == x.symmetric_difference(y)
    True
    """
    x, y = set(x), set(y)
    union = x.union(y)
    intersection = x.intersection(y)
    in_x_but_not_y = x.difference(y)
    in_y_but_not_x = y.difference(x)
    symmetric_diff = x ^ y
    jaccard = len(intersection) / len(union)
    overlap = len(intersection) / min(len(x), len(y))

    output = {
        "x": x,
        "y": y,
        "x | y": union,
        "x & y": intersection,
        "x - y": in_x_but_not_y,
        "y - x": in_y_but_not_x,
        "x ^ y": symmetric_diff,
        "jaccard": jaccard,
        "overlap": overlap,
    }

    lines = []
    for k, v in output.items():
        if isinstance(v, set):
            elements = f"{sorted(v)[:show]}".replace("[", "{")
            elements = (
                elements.replace("]", ", ...}")
                if len(v) > show
                else elements.replace("]", "}")
            )
            elements = elements.replace(",", "") if len(v) == 1 else elements
            desc = f"{k} (n={len(v)})"
            if k in ["x", "y"]:
                desc = f"    {desc}"
            msg = f"{desc}: {elements}"
            lines.append(msg)

        else:
            lines.append(f"{k} = {v:g}")

    tmp = {
        "disjoint?": x.isdisjoint(y),
        "x == y": x == y,
        "x <= y": x <= y,
        "x <  y": x < y,
        "y <= x": y <= x,
        "y <  x": y < x,
    }

    for k, v in tmp.items():
        lines.append(f"{k}: {v}")

    output.update(tmp)
    output["report"] = "\n".join(lines)

    return output
