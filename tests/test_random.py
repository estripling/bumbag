from random import Random

import pytest

from bumbag import random


@pytest.mark.parametrize("arg", [None, 0, Random(1), "invalid seed"])
def test_get_random_instance(arg):
    seed = arg
    if seed is None or isinstance(seed, (int, Random)):
        assert isinstance(random.get_random_instance(seed), Random)
    else:
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            random.get_random_instance(seed)


@pytest.mark.parametrize("arg", [0.25, 0.5, 0.75, -0.1, 1.1, 11])
def test_coinflip(arg):
    bias = arg
    if 0 <= bias <= 1:
        actual = {random.coinflip() for _ in range(30)}
        expected = {True, False}
        assert actual == expected
    else:
        with pytest.raises(ValueError):
            random.coinflip(bias)


def test_get_random_integer():
    for _ in range(10):
        rnd_int = random.get_random_integer()
        assert isinstance(rnd_int, int)
        assert 0 <= rnd_int <= 2147483647
