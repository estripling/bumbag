from string import punctuation


def remove_punctuation(string):
    """Remove punctuation from a string.

    Parameters
    ----------
    string : str
        String to be processed.

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
