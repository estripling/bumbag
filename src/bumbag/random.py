import random
import string

__all__ = (
    "coinflip",
    "get_random_character",
    "get_random_instance",
    "get_random_integer",
)


def coinflip(*, bias=0.5, seed=None):
    """Flip a coin.

    Parameters
    ----------
    bias : float, default=0.5
        Specify the bias of the coin:
         - A ``bias`` of 0.5 corresponds to a fair coin.
         - A ``bias`` closer to 1.0 is more likely to generate ``True``.
         - A ``bias`` closer to 0.0 is more likely to generate ``False``.
    seed : None, int, random.Random, default=None
        Value to seed an instance:
         - If ``seed`` is None, return random module's singleton.
         - If ``seed`` is an integer, return a new instance seeded with it.
         - If ``seed`` is already a Random instance, return the instance.

    Returns
    -------
    bool
        Outcome of the digital coin flip.

    Raises
    ------
    ValueError
        If ``bias`` is not in [0, 1].

    Examples
    --------
    >>> import bumbag
    >>> {bumbag.coinflip() for _ in range(30)} == {True, False}
    True
    """
    if not (0 <= bias <= 1):
        raise ValueError(f"{bias=} - must be a float in [0, 1]")
    rng = get_random_instance(seed=seed)
    return rng.random() < bias


def get_random_character(alphabet=None, /, *, seed=None):
    """Get a random character from a given alphabet.

    Parameters
    ----------
    alphabet : str, default=None
        Set of characters to sample from.
        If None, the default alphabet is made of [a-zA-Z0-9] characters.
    seed : None, int, random.Random, default=None
        Value to seed an instance:
         - If ``seed`` is None, return random module's singleton.
         - If ``seed`` is an integer, return a new instance seeded with it.
         - If ``seed`` is already a Random instance, return the instance.

    Returns
    -------
    str
        A random character.

    Examples
    --------
    >>> import bumbag
    >>> rnd_char = bumbag.get_random_character("bumbag")
    >>> isinstance(rnd_char, str)
    True
    >>> rnd_char in "bumbag"
    True
    """
    rng = get_random_instance(seed=seed)
    alphabet = alphabet or string.ascii_letters + string.digits
    return rng.sample(population=alphabet, k=len(alphabet))[0]


def get_random_instance(*, seed=None):
    """Turn seed into a random.Random instance.

    Parameters
    ----------
    seed : None, int, random.Random, default=None
        Value to seed an instance:
         - If ``seed`` is None, return random module's singleton.
         - If ``seed`` is an integer, return a new instance seeded with it.
         - If ``seed`` is already a Random instance, return the instance.

    Returns
    -------
    random.Random
        A random number generator instance.

    Raises
    ------
    ValueError
        If ``seed`` cannot be used to seed a Random instance.

    Notes
    -----
    Inspired by the ``check_random_state`` function of scikit-learn.

    Examples
    --------
    >>> import bumbag
    >>> import random
    >>> rng = bumbag.get_random_instance()
    >>> isinstance(rng, random.Random)
    True
    """
    random_singleton = getattr(random, "_inst")
    if seed is None or seed is random_singleton:
        return random_singleton

    elif isinstance(seed, int):
        return random.Random(seed)

    elif isinstance(seed, random.Random):
        return seed

    else:
        raise ValueError(f"{seed=} cannot be used to seed a Random instance")


def get_random_integer(a=0, b=2147483647, /, *, seed=None):
    """Get a random integer from interval [a, b].

    Setting default values for the arguments of ``random.randint``.

    Parameters
    ----------
    a : int, default=0
        Lower endpoint of interval.
    b : int, default=2147483647
        Upper endpoint of interval.
    seed : None, int, random.Random, default=None
        Value to seed an instance:
         - If ``seed`` is None, return random module's singleton.
         - If ``seed`` is an integer, return a new instance seeded with it.
         - If ``seed`` is already a Random instance, return the instance.

    Returns
    -------
    int
        A random integer.

    Examples
    --------
    >>> import bumbag
    >>> rnd_int = bumbag.get_random_integer()
    >>> isinstance(rnd_int, int)
    True
    >>> 0 <= rnd_int <= 2147483647
    True
    """
    rng = get_random_instance(seed=seed)
    return rng.randint(a, b)
