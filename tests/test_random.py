import string
from random import Random

import pytest

import bumbag as bb


@pytest.mark.parametrize("arg", [0.25, 0.5, 0.75, -0.1, 1.1, 11])
def test_coinflip(arg):
    bias = arg
    if 0 <= bias <= 1:
        actual = {bb.coinflip() for _ in range(30)}
        expected = {True, False}
        assert actual == expected
    else:
        with pytest.raises(ValueError):
            bb.coinflip(bias)


def test_get_random_character():
    alphabet = string.ascii_letters + string.digits
    rnd_char = bb.get_random_character()
    assert isinstance(rnd_char, str)
    assert rnd_char in alphabet


@pytest.mark.parametrize("arg", [None, 0, Random(1), "invalid seed"])
def test_get_random_instance(arg):
    seed = arg
    if seed is None or isinstance(seed, (int, Random)):
        assert isinstance(bb.get_random_instance(seed), Random)
    else:
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            bb.get_random_instance(seed)


def test_get_random_integer():
    for _ in range(10):
        rnd_int = bb.get_random_integer()
        assert isinstance(rnd_int, int)
        assert 0 <= rnd_int <= 2147483647
