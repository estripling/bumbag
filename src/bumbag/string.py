import functools
import re
from string import punctuation

import toolz


@toolz.curry
def filter_regex(pattern, collection, flags=re.IGNORECASE):
    """Filter collection of strings with a regex pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern to use.
    collection : list of str
        A collection of strings to filter according to the ``pattern``.
    flags : RegexFlag, default=re.IGNORECASE
        Regex flag passed to ``re.findall`` function.
        See official Python documentation for more information.

    Yields
    ------
    str
        A generator of the original string values of the collection,
        containing those values where the string matches the regex pattern.

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
    >>> filter_python_regex = filter_regex("python")
    >>> list(filter_python_regex(list_of_strings))
    ["Guiding principles for Python's design: The Zen of Python"]
    """
    func = functools.partial(re.findall, pattern, flags=flags)
    return filter(func, collection)


@toolz.curry
def map_regex(pattern, collection, flags=re.IGNORECASE):
    """Map regex pattern to a collection of strings.

    Parameters
    ----------
    pattern : str
        Regex pattern to use.
    collection : list of str
        A collection of strings to match ``pattern`` against it.
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
    >>> map_python_regex = map_regex("python")
    >>> list(map_python_regex(list_of_strings))
    [['Python', 'Python'], [], [], []]
    """
    func = functools.partial(re.findall, pattern, flags=flags)
    return map(func, collection)


def remove_punctuation(string):
    """Remove punctuation from a string.

    Parameters
    ----------
    string : str
        String to process.

    Returns
    -------
    str
        String with punctuation removed.

    Examples
    --------
    >>> remove_punctuation("I think, therefore I am. --Descartes")
    'I think therefore I am Descartes'
    """
    return string.translate(str.maketrans("", "", punctuation))
