import collections
import inspect
import math
import operator
from typing import Generator

import toolz


@toolz.curry
def extend_range(min_value, max_value, min_factor=0.05, max_factor=0.05):
    """Extend value range by a factor.

    The value range is defined as ``max_value - min_value``.

    Parameters
    ----------
    min_value : int, float
        Lower endpoint of value range.
    max_value : int, float
        Upper endpoint of value range.
    min_factor : float, default=0.05
        Factor w.r.t. value range to extend the lower endpoint.
    max_factor : float, default=0.05
        Factor w.r.t. value range to extend the upper endpoint.

    Returns
    -------
    tuple of float
        Endpoints of extended value range.

    Notes
    -----
    - Function is curried.
    - If ``min_value > max_value``, swapping values.

    Examples
    --------
    >>> extend_range(0, 1)
    (-0.05, 1.05)

    >>> extend_range(0, 1, 0.1, 0.2)
    (-0.1, 1.2)
    """
    if not isinstance(min_factor, float) or min_factor < 0:
        raise ValueError(f"{min_factor=} - must be a non-negative number")

    if not isinstance(max_factor, float) or max_factor < 0:
        raise ValueError(f"{max_factor=} - must be a non-negative number")

    min_value, max_value = sorted([min_value, max_value])
    value_range = max_value - min_value

    new_min_value = min_value - (min_factor * value_range)
    new_max_value = max_value + (max_factor * value_range)

    return new_min_value, new_max_value


def flatten(*sequences):
    """Flatten an arbitrarily nested and possibly irregular collection.

    Parameters
    ----------
    sequences : collection
        Collection of sequences and/or items to flatten.

    Yields
    ------
    Any
        A generator of flattened collection items.

    Notes
    -----
    A string is not treated as a sequence.

    Examples
    --------
    >>> list(flatten([1, 2, 3]))
    [1, 2, 3]

    >>> list(flatten(*[1, 2, 3]))
    [1, 2, 3]

    >>> list(flatten(1, 2, 3))
    [1, 2, 3]

    >>> list(flatten([1, 2], 3))
    [1, 2, 3]

    >>> list(flatten([1, (2, 3)], 4, [], [[[5]], 6]))
    [1, 2, 3, 4, 5, 6]

    >>> list(flatten([[1, (2, 3)], 4, [], [[[5]], 6]]))
    [1, 2, 3, 4, 5, 6]

    >>> list(flatten(["one", 2], 3, [(4, "five")], [[["six"]]], "seven", []))
    ['one', 2, 3, 4, 'five', 'six', 'seven']

    >>> list(flatten([-1], 0, range(1, 4)))
    [-1, 0, 1, 2, 3]

    >>> list(flatten([-1], 0, map(lambda x: 2 * x, range(1, 4))))
    [-1, 0, 2, 4, 6]

    >>> generator_comprehension = (2 * x for x in range(1, 4))  # noqa
    >>> list(flatten([[-1], 0], generator_comprehension))
    [-1, 0, 2, 4, 6]

    >>> list(flatten([-1], 0, filter(lambda x: x % 2 == 0, range(1, 7))))
    [-1, 0, 2, 4, 6]
    """

    def flattenit(seqs):
        iterator_types_to_flatten = (
            Generator,
            filter,
            list,
            map,
            range,
            tuple,
        )

        for seq in seqs:
            if isinstance(seq, iterator_types_to_flatten):
                yield from flattenit(seq)
            else:
                yield seq

    return flattenit(sequences)


def freq(values):
    """Compute value frequencies.

    Given a collection of values, calculate for each value:
     - the frequency (``n``),
     - the cumulative frequency (``N``),
     - the relative frequency (``r``), and
     - the cumulative relative frequency (``R``).

    Parameters
    ----------
    values : iterable
        Collection of values, where each value must be of an immutable type
        that can be used as a dictionary key.

    Returns
    -------
    dict of dict
        Frequencies of each distinct value.

    Examples
    --------
    >>> x = ["a", "c", "b", "g", "h", "a", "g", "a"]
    >>> frequency = freq(x)
    >>> isinstance(frequency, dict)
    True
    >>> frequency["n"]
    {'a': 3, 'g': 2, 'c': 1, 'b': 1, 'h': 1}
    >>> frequency["N"]
    {'a': 3, 'g': 5, 'c': 6, 'b': 7, 'h': 8}
    >>> frequency["r"]
    {'a': 0.375, 'g': 0.25, 'c': 0.125, 'b': 0.125, 'h': 0.125}
    >>> frequency["R"]
    {'a': 0.375, 'g': 0.625, 'c': 0.75, 'b': 0.875, 'h': 1.0}
    >>> freq("acbghaga") == frequency
    True

    >>> x = [1, "c", False, 2.0, None, 1, 2.0, 1]
    >>> frequency = freq(x)
    >>> frequency["n"]
    {1: 3, 2.0: 2, 'c': 1, False: 1, None: 1}
    """
    output = dict()
    counter = collections.Counter(values)
    distinct_values, frequencies = zip(*counter.most_common(len(counter)))

    cumsum = toolz.curried.accumulate(operator.add)
    div_by_total = op(operator.truediv, y=sum(frequencies))
    relative = toolz.curried.map(div_by_total)

    output["n"] = dict(zip(distinct_values, frequencies))
    output["N"] = dict(zip(distinct_values, cumsum(frequencies)))
    output["r"] = dict(zip(distinct_values, relative(frequencies)))
    output["R"] = dict(zip(distinct_values, cumsum(relative(frequencies))))

    return output


def get_function_name():
    """Get name of the function when in its body.

    Returns
    -------
    str
        Name of the function.

    Examples
    --------
    >>> def my_test_function():
    ...     return get_function_name()
    ...
    >>> my_test_function()
    'my_test_function'
    """
    return inspect.stack()[1].function


def get_source_code(obj):
    """Get source code of an object.

    Parameters
    ----------
    obj : module, class, method, function, traceback, frame, or code object
        Object to get source code from.

    Returns
    -------
    str
        Source code of the object.

    Examples
    --------
    >>> def my_test_function():
    ...     return "Hello, World!"
    ...
    >>> print(get_source_code(my_test_function))
    def my_test_function():
        return "Hello, World!"
    <BLANKLINE>
    """
    return inspect.getsource(obj)


@toolz.curry
def op(func, x, y):
    """Apply an operator function that takes two inputs.

    Parameters
    ----------
    func : function
        Operator function to use.
    x : Any
        First argument of the function.
    y : Any
        Second argument of the function.

    Returns
    -------
    function or Any
        Output value of ``func`` if both ``x`` and ``y`` are given
        or a curried version of ``func`` if either ``x`` or ``y`` is given.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> from operator import add
    >>> inc = op(add, 1)
    >>> inc(0)
    1

    >>> inc(10)
    11
    """
    return func(x, y)


@toolz.curry
def sig(number, digits=3):
    """Round number to its significant digits.

    Parameters
    ----------
    number : int, float
        Number to round.
    digits : int, default=3
        Number of significant digits.

    Returns
    -------
    int, float
        Number rounded to its significant digits.

    Raises
    ------
    ValueError
        If ``digits`` is not a positive integer.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> sig(987654321)
    988000000

    >>> sig(14393237.76, 2)
    14000000.0

    >>> sig(14393237.76, 3)
    14400000.0
    """
    if not isinstance(digits, int) or digits < 1:
        raise ValueError(f"{digits=} - must be a positive integer")

    if not math.isfinite(number) or math.isclose(number, 0.0):
        return number

    digits -= math.ceil(math.log10(abs(number)))
    return round(number, digits)


def two_set_summary(x, y, show=3):
    """Compute two set summary.

    Given two sets, calculate multiple key set operations like union,
    intersection, difference, and more.

    Parameters
    ----------
    x : set
        Left set.
    y : set
        Right set.
    show : int, default=3
        Specify how many elements per set to show in report.

    Returns
    -------
    dict of sets
        Summary of two sets.

    References
    ----------
    .. [1] "Basic set operations", Wikipedia,
           `<https://en.wikipedia.org/wiki/Set_(mathematics)#Basic_operations>`_
    .. [2] "Jaccard index", Wikipedia,
           https://en.wikipedia.org/wiki/Jaccard_index
    .. [3] "Overlap coefficient", Wikipedia,
           https://en.wikipedia.org/wiki/Overlap_coefficient
    .. [4] "Dice similarity coefficient", Wikipedia,
           `<https://en.wikipedia.org/wiki/Sørensen–Dice_coefficient>`_

    Examples
    --------
    >>> a = {"a", "c", "b", "g", "h"}
    >>> b = {"c", "d", "e", "f", "g"}
    >>> summary = two_set_summary(a, b)
    >>> isinstance(summary, dict)
    True
    >>> summary["x"] == a
    True
    >>> summary["y"] == b
    True
    >>> summary["x | y"] == a.union(b)
    True
    >>> summary["x & y"] == a.intersection(b)
    True
    >>> summary["x - y"] == a.difference(b)
    True
    >>> summary["y - x"] == b.difference(a)
    True
    >>> summary["x ^ y"] == a.symmetric_difference(b)
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
    dice = 2 * len(intersection) / (len(x) + len(y))

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
        "dice": dice,
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
