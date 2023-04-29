import functools
import inspect
import math
import operator
from collections import Counter
from typing import Iterator, Sequence

from toolz import curried

__all__ = (
    "all_predicate_true",
    "any_predicate_true",
    "extend_range",
    "flatten",
    "freq",
    "get_function_name",
    "get_source_code",
    "numberformat",
    "op",
    "setred",
    "sig",
    "two_set_summary",
)


@curried.curry
def all_predicate_true(predicates, x, /):
    """Check if all predicates are true.

    Parameters
    ----------
    predicates : Iterable of Callable[[Any], bool]]
        Collection of predicates to check.
    x : Any
        Specify the value to evaluate the predicates on.

    Returns
    -------
    bool
        ``True`` if all predicates evaluate to ``True`` else ``False``.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> import bumbag
    >>> is_divisible_by_3_and_5 = bumbag.all_predicate_true(
    ...     [lambda n: n % 3 == 0, lambda n: n % 5 == 0]
    ... )
    >>> is_divisible_by_3_and_5(60)
    True
    >>> is_divisible_by_3_and_5(9)
    False
    """
    return all(predicate(x) for predicate in predicates)


@curried.curry
def any_predicate_true(predicates, x, /):
    """Check if any predicate is true.

    Parameters
    ----------
    predicates : Iterable of Callable[[Any], bool]]
        Collection of predicates to check.
    x : Any
        Specify the value to evaluate the predicates on.

    Returns
    -------
    bool
        ``True`` if any predicate evaluates to ``True`` else ``False``.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> import bumbag
    >>> is_divisible_by_3_or_5 = bumbag.any_predicate_true(
    ...     [lambda n: n % 3 == 0, lambda n: n % 5 == 0]
    ... )
    >>> is_divisible_by_3_or_5(60)
    True
    >>> is_divisible_by_3_or_5(9)
    True
    >>> is_divisible_by_3_or_5(13)
    False
    """
    return any(predicate(x) for predicate in predicates)


@curried.curry
def extend_range(min_value, max_value, /, *, min_factor=0.05, max_factor=0.05):
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
    >>> import bumbag
    >>> bumbag.extend_range(0, 1)
    (-0.05, 1.05)

    >>> bumbag.extend_range(0, 1, min_factor=0.1, max_factor=0.2)
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
    """Flatten arbitrarily nested sequences.

    Parameters
    ----------
    sequences : Any, Iterator, Sequence
        Arbitrarily nested sequences of possibly heterogeneous data types
        to flatten. If an object in ``sequences`` is not of type Iterator or
        Sequence, the object itself is returned. Note that a string, albeit
        being of type Sequence, is not further processed but is immediately
        returned instead.

    Yields
    ------
    Any
        A generator of objects of flattened sequences.

    Examples
    --------
    >>> import bumbag
    >>> list(bumbag.flatten([1, 2, 3]))
    [1, 2, 3]

    >>> list(bumbag.flatten((1, 2, 3)))
    [1, 2, 3]

    >>> list(bumbag.flatten(*[1, 2, 3]))
    [1, 2, 3]

    >>> list(bumbag.flatten(1, 2, 3))
    [1, 2, 3]

    >>> list(bumbag.flatten([1, 2], 3))
    [1, 2, 3]

    >>> list(bumbag.flatten([1, (2, 3)], 4, [], [[[5]], 6]))
    [1, 2, 3, 4, 5, 6]

    >>> list(bumbag.flatten([[1, (2, 3)], 4, [], [[[5]], 6]]))
    [1, 2, 3, 4, 5, 6]

    >>> list(bumbag.flatten([iter([1, iter((2, 3))]), 4, [], iter([[[5]], 6])]))
    [1, 2, 3, 4, 5, 6]

    >>> list(bumbag.flatten(["one", 2], 3, [(4, "five")], [[["six"]]], "seven", []))
    ['one', 2, 3, 4, 'five', 'six', 'seven']

    >>> list(bumbag.flatten([-1], 0, range(1, 4)))
    [-1, 0, 1, 2, 3]

    >>> list(bumbag.flatten([-1], 0, map(lambda x: 2 * x, range(1, 4))))
    [-1, 0, 2, 4, 6]

    >>> generator_expression = (2 * x for x in range(1, 4))  # noqa
    >>> list(bumbag.flatten([[-1], 0], generator_expression))
    [-1, 0, 2, 4, 6]

    >>> list(bumbag.flatten([-1], 0, filter(lambda x: x % 2 == 0, range(1, 7))))
    [-1, 0, 2, 4, 6]
    """

    def flattenit(iterables):
        for i in iterables:
            if isinstance(i, (Iterator, Sequence)) and not isinstance(i, str):
                yield from flattenit(i)
            else:
                yield i

    return flattenit(sequences)


def freq(values):
    """Compute value frequencies.

    Given an iterable of values, calculate for each distinct value:
     - the frequency (``n``),
     - the cumulative frequency (``N``),
     - the relative frequency (``r``), and
     - the cumulative relative frequency (``R``).

    Parameters
    ----------
    values : Iterable of Any
        An iterable of values to compute the frequencies of its members.

    Returns
    -------
    dict
        A dictionary with its keys being the frequency type and its values
        being dictionaries with the frequencies of the distinct values of the
        iterable.

    Examples
    --------
    >>> import bumbag
    >>> x = ["a", "c", "b", "g", "h", "a", "g", "a"]
    >>> frequency = bumbag.freq(x)
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
    >>> bumbag.freq("acbghaga") == frequency
    True

    >>> x = [1, "c", False, 2.0, None, 1, 2.0, 1]
    >>> frequency = bumbag.freq(x)
    >>> frequency["n"]
    {1: 3, 2.0: 2, 'c': 1, False: 1, None: 1}
    """
    output = dict()
    distinct_values, frequencies = zip(*Counter(iter(values)).most_common())

    cumsum = curried.accumulate(operator.add)
    div_by_total = op(operator.truediv, y=sum(frequencies))
    relative = curried.map(div_by_total)

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
    >>> import bumbag
    >>> def my_test_function():
    ...     return bumbag.get_function_name()
    ...
    >>> my_test_function()
    'my_test_function'
    """
    return inspect.stack()[1].function


def get_source_code(obj, /):
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
    >>> import bumbag
    >>> def my_test_function():
    ...     return "Hello, World!"
    ...
    >>> print(bumbag.get_source_code(my_test_function))
    def my_test_function():
        return "Hello, World!"
    <BLANKLINE>
    """
    return inspect.getsource(obj)


def numberformat(number, /):
    """Format numeric literals with underscores.

    Parameters
    ----------
    number : int or float
        Number to format.

    Returns
    -------
    str
        A string representation with underscores of a numeric literal.

    Examples
    --------
    >>> import bumbag
    >>> bumbag.numberformat(1000000)
    '1_000_000'

    >>> bumbag.numberformat(100000.0)
    '100_000.0'
    """
    return f"{number:,}".replace(",", "_")


@curried.curry
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
    >>> import bumbag
    >>> import operator
    >>> inc = bumbag.op(operator.add, 1)
    >>> inc(0)
    1

    >>> inc(10)
    11
    """
    return func(x, y)


@curried.curry
def setred(func, *sets):
    """Apply a set function to reduce a sequence of sets.

    Parameters
    ----------
    func : function
        Specify the set function.
    sets : set
        A sequence of Python set objects to reduce.

    Returns
    -------
    set
        A reduced set according to the set function.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> import bumbag
    >>> x = {0, 1, 2, 3}
    >>> y = {2, 4, 6}
    >>> z = {2, 6, 8}
    >>> bumbag.setred(set.intersection, x, y, z)
    {2}

    >>> bumbag.setred(set.union, x, y, z)
    {0, 1, 2, 3, 4, 6, 8}

    >>> bumbag.setred(set.difference, x, y, z)
    {0, 1, 3}

    >>> sym_diff = bumbag.setred(set.symmetric_difference)
    >>> sym_diff(x, y, z)
    {0, 1, 2, 3, 4, 8}
    """
    return functools.reduce(func, map(set, sets))


@curried.curry
def sig(number, /, *, digits=3):
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
    >>> import bumbag
    >>> bumbag.sig(987654321)
    988000000

    >>> bumbag.sig(14393237.76, digits=2)
    14000000.0

    >>> bumbag.sig(14393237.76, digits=3)
    14400000.0
    """
    if not isinstance(digits, int) or digits < 1:
        raise ValueError(f"{digits=} - must be a positive integer")

    if not math.isfinite(number) or math.isclose(number, 0.0):
        return number

    digits -= math.ceil(math.log10(abs(number)))
    return round(number, digits)


def two_set_summary(x, y, /, *, show=3):
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
    >>> import bumbag
    >>> a = {"a", "c", "b", "g", "h"}
    >>> b = {"c", "d", "e", "f", "g"}
    >>> summary = bumbag.two_set_summary(a, b)
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
