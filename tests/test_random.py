import string
from random import Random

import pytest

import bumbag


@pytest.mark.parametrize("arg", [0.25, 0.5, 0.75, -0.1, 1.1, 11])
def test_coinflip(arg):
    bias = arg
    if 0 <= bias <= 1:
        actual = {bumbag.coinflip() for _ in range(30)}
        expected = {True, False}
        assert actual == expected
    else:
        with pytest.raises(ValueError):
            bumbag.coinflip(bias=bias)


def test_get_random_character():
    alphabet = string.ascii_letters + string.digits
    rnd_char = bumbag.get_random_character()
    assert isinstance(rnd_char, str)
    assert rnd_char in alphabet


@pytest.mark.parametrize("arg", [None, 0, Random(1), "invalid seed"])
def test_get_random_instance(arg):
    seed = arg
    if seed is None or isinstance(seed, (int, Random)):
        assert isinstance(bumbag.get_random_instance(seed=seed), Random)
    else:
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            bumbag.get_random_instance(seed=seed)


def test_get_random_integer():
    for _ in range(10):
        rnd_int = bumbag.get_random_integer()
        assert isinstance(rnd_int, int)
        assert 0 <= rnd_int <= 2147483647
