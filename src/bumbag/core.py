import inspect
import math
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
