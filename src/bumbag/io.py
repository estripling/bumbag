from distutils.util import strtobool


def query_yes_no(question, default=None):
    """Prompt user a yes/no question.

    Parameters
    ----------
    question: str
        Specify a yes/no question to prompt the user.
    default: None, str, default=None
        Define default answer:
         - If ``default`` is None, an explicit answer is needed from the user.
         - If ``default`` is "yes" or "no", the presumed answer, indicated by
           a capitial letter, is accepted when pressing <enter>.

    Returns
    -------
    bool
        True if user's answer is yes.
        False if user's answer is no.

    Raises
    ------
    ValueError
        If ``default`` is none of the following values: {None, 'yes', 'no'}.

    Examples
    --------
    >>> query_yes_no("Is all clear?")  # doctest: +SKIP
    Is all clear? [y/n] y<enter>
    True

    >>> query_yes_no("Do you like BumBag?", "yes")  # doctest: +SKIP
    Do you like BumBag? [Y/n] <enter>
    True

    >>> query_yes_no("Do you like BumBag?", "yes")  # doctest: +SKIP
    Do you like BumBag? [Y/n] yay<enter>
    Do you like BumBag? Please respond with 'yes' [Y] or 'no' [n] <enter>
    True
    """
    prompt = (
        "[y/n]"
        if default is None
        else "[Y/n]"
        if default == "yes"
        else "[y/N]"
        if default == "no"
        else "invalid"
    )

    if prompt == "invalid":
        raise ValueError(f"{default=} - must be either None, 'yes', or 'no'")

    answer = input(f"{question} {prompt} ").lower()

    while True:
        try:
            if answer == "" and default in ["yes", "no"]:
                return bool(strtobool(default))
            return bool(strtobool(answer))

        except ValueError:
            msg = "{} Please respond with 'yes' [{}] or 'no' [{}] ".format(
                question,
                "Y" if default == "yes" else "y",
                "N" if default == "no" else "n",
            )
            answer = input(msg).lower()
