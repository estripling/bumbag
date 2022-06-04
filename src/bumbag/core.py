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
