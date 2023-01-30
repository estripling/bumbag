import functools
import re
import string as builtin_string_module

import toolz

__all__ = (
    "filter_regex",
    "map_regex",
    "remove_punctuation",
)


@toolz.curry
def filter_regex(pattern, strings, flags=re.IGNORECASE):
    """Filter an iterable of strings with a regex pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern to use.
    strings : Iterable of str
        An iterable of strings to filter according to ``pattern``.
    flags : RegexFlag, default=re.IGNORECASE
        Regex flag passed to ``re.findall`` function.
        See official Python documentation for more information.

    Yields
    ------
    str
        A generator returning the original string if there is a match.

    Notes
    -----
    Function is curried.

    References
    ----------
    .. [1] "Regular expression operations", Official Python documentation,
           https://docs.python.org/3/library/re.html

    Examples
    --------
    >>> import bumbag
    >>> list_of_strings = [
    ...     "Guiding principles for Python's design: The Zen of Python",
    ...     "Beautiful is better than ugly.",
    ...     "Explicit is better than implicit.",
    ...     "Simple is better than complex.",
    ... ]
    >>> filter_python_regex = bumbag.filter_regex("python")
    >>> list(filter_python_regex(list_of_strings))
    ["Guiding principles for Python's design: The Zen of Python"]
    """
    return filter(functools.partial(re.findall, pattern, flags=flags), strings)


@toolz.curry
def map_regex(pattern, strings, flags=re.IGNORECASE):
    """Map regex pattern to an iterable of strings.

    Parameters
    ----------
    pattern : str
        Regex pattern to use.
    strings : Iterable of str
        An iterable of strings to match ``pattern`` against its members.
    flags : RegexFlag, default=re.IGNORECASE
        Regex flag passed to ``re.findall`` function.
        See official Python documentation for more information.

    Yields
    ------
    str
        A generator returning the matches per string. If there is a match for a
        given string, a list of all occurrences of the pattern is returned.
        The list is empty if there is no match.

    Notes
    -----
    Function is curried.

    References
    ----------
    .. [1] "Regular expression operations", Official Python documentation,
           https://docs.python.org/3/library/re.html

    Examples
    --------
    >>> import bumbag
    >>> list_of_strings = [
    ...     "Guiding principles for Python's design: The Zen of Python",
    ...     "Beautiful is better than ugly.",
    ...     "Explicit is better than implicit.",
    ...     "Simple is better than complex.",
    ... ]
    >>> map_python_regex = bumbag.map_regex("python")
    >>> list(map_python_regex(list_of_strings))
    [['Python', 'Python'], [], [], []]
    """
    return map(functools.partial(re.findall, pattern, flags=flags), strings)


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
    >>> import bumbag
    >>> bumbag.remove_punctuation("I think, therefore I am. --Descartes")
    'I think therefore I am Descartes'
    """
    return string.translate(str.maketrans("", "", builtin_string_module.punctuation))
