import random


def get_random_instance(seed=None):
    """Turn seed into a random.Random instance.

    Parameters
    ----------
    seed : None, int, random.Random, default=None
        Value used to seed a Random instance:
         - If ``seed`` is None, return the Random singleton used by random.
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
    >>> import random
    >>> prng = get_random_instance()
    >>> isinstance(prng, random.Random)
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


def coinflip(bias=0.5, seed=None):
    """Flip a coin.

    Parameters
    ----------
    bias : float, default=0.5
        Specify the bias of the coin:
         - A ``bias`` of 0.5 corresponds to a fair coin.
         - A ``bias`` closer to 1.0 is more likely to generate ``True``.
         - A ``bias`` closer to 0.0 is more likely to generate ``False``.
    seed : None, int, random.Random, default=None
        Value used to seed a Random instance:
         - If ``seed`` is None, return the Random singleton used by random.
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
    >>> {coinflip() for _ in range(30)} == {True, False}
    True
    """
    if not (0 <= bias <= 1):
        raise ValueError(f"{bias=} must be a float in [0, 1]")
    rng = get_random_instance(seed)
    return rng.random() < bias
