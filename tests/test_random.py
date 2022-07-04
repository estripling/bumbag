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
