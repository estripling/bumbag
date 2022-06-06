import functools
import inspect
import math
import re
from string import punctuation

from toolz import curry


def remove_punctuation(text: str) -> str:
    """Remove punctuation from a string.

    Parameters
    ----------
    text : str
        Text to be processed.

    Returns
    -------
    str
        Text with punctuation removed.

    Examples
    --------
    >>> remove_punctuation("I think, therefore I am. --Descartes")
    'I think therefore I am Descartes'
    """
    return text.translate(str.maketrans("", "", punctuation))


@curry
def op(func, x, y):
    """Curry a binary function to perform an operation.

    Parameters
    ----------
    func : function
        A binary function.
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
    >>> add1 = op(add, 1)
    >>> add1(0)
    1
    >>> add1(10)
    11
    """
    return func(x, y)


@curry
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
        Number rouned to its significant digits.

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
        raise ValueError(f"digits={digits} - must be a positive integer")

    if not math.isfinite(number) or math.isclose(number, 0.0):
        return number

    digits -= math.ceil(math.log10(abs(number)))
    return round(number, digits)


@curry
def extend_range(vmin, vmax, pmin=0.05, pmax=0.05):
    """Extend range by small percentage.

    Parameters
    ----------
    vmin : int, float
        Lower endpoint of range.
    vmax : int, float
        Upper endpoint of range.
    pmin : float, default=0.05
        Percentage to extend the lower endpoint.
    pmax : float, default=0.05
        Percentage to extend the lower endpoint.

    Returns
    -------
    tuple of float
        Endpoints of extended range.

    Notes
    -----
    Function is curried.

    Examples
    --------
    >>> extend_range(0, 1)
    (-0.05, 1.05)
    """
    if not isinstance(pmin, float) or pmin < 0:
        raise ValueError(f"pmin={pmin} - must be a non-negative number")

    if not isinstance(pmax, float) or pmax < 0:
        raise ValueError(f"pmax={pmax} - must be a non-negative number")

    delta = vmax - vmin
    new_vmin = vmin - (pmin * delta)
    new_vmax = vmax + (pmax * delta)
    return new_vmin, new_vmax


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
    >>> my_test_function()
    'my_test_function'
    """
    return inspect.stack()[1].function


@curry
def mapregex(pattern, collection, flags=re.IGNORECASE):
    """Map regex pattern to each string element of a collection.

    Parameters
    ----------
    pattern : str
        Regex pattern.
    collection : list of str
        A collection of strings to match ``pattern`` against.
    flags : RegexFlag, default=re.IGNORECASE
        Regex flag passed to ``re.findall`` function.
        See official Python documentation for more information.

    Yields
    ------
    str
        A generator of matches where each match corresponds to a list of all
        non-overlapping matches in the string.

    Notes
    -----
    Function is curried.

    References
    ----------
    .. [1] "Regular expression operations", Official Python documentation,
           https://docs.python.org/3/library/re.html

    Examples
    --------
    >>> list_of_strings = [
    ...     "Guiding principles for Python's design: The Zen of Python",
    ...     "Beautiful is better than ugly.",
    ...     "Explicit is better than implicit",
    ...     "Simple is better than complex.",
    ... ]
    >>> mapregex_python = mapregex("python")
    >>> list(mapregex_python(list_of_strings))
    [['Python', 'Python'], [], [], []]
    """
    func = functools.partial(re.findall, pattern, flags=flags)
    return map(func, collection)


@curry
def filterregex(pattern, collection, flags=re.IGNORECASE):
    """Filter collection of strings based on regex pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern.
    collection : list of str
        A collection of strings to match ``pattern`` against.
    flags : RegexFlag, default=re.IGNORECASE
        Regex flag passed to ``re.findall`` function.
        See official Python documentation for more information.

    Yields
    ------
    str
        A generator of the original strings in the collection
        for which there is a match with the regex pattern.

    Notes
    -----
    Function is curried.

    References
    ----------
    .. [1] "Regular expression operations", Official Python documentation,
           https://docs.python.org/3/library/re.html

    Examples
    --------
    >>> list_of_strings = [
    ...     "Guiding principles for Python's design: The Zen of Python",
    ...     "Beautiful is better than ugly.",
    ...     "Explicit is better than implicit",
    ...     "Simple is better than complex.",
    ... ]
    >>> filterregex_python = filterregex("python")
    >>> list(filterregex_python(list_of_strings))
    ["Guiding principles for Python's design: The Zen of Python"]
    """
    func = functools.partial(re.findall, pattern, flags=flags)
    return filter(func, collection)
