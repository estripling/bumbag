# Author: Eugen Stripling <estripling042@gmail.com>
# License: BSD 3 clause

import collections
import functools
import operator
import pathlib
import random
import statistics
import string
import timeit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from toolz import curried, curry

from bumbag import core


def main():
    num_runs = 100
    num_repetitions = 10

    runtimes = get_runtimes(
        functions=(freq_pd, enhanced_value_counts),
        sample_sizes=(100, 1000, 10000, 100000, 1000000),
        num_runs=num_runs,
        num_repetitions=num_repetitions,
        rng=np.random.RandomState(2022),
    )
    fig, _ = plot(runtimes, num_runs, num_repetitions)
    path = pathlib.Path(__file__).stem + ".png"
    plt.savefig(path, dpi=300)


def plot(runtimes, num_runs, num_repetitions):
    fig, ax = plt.subplots(1, 1, figsize=(7, 6))

    sizes = runtimes["sample_sizes"]
    for name, values in runtimes.items():
        if name != "sample_sizes":
            ax.plot(sizes, values, marker="o", label=name)

    ax.legend(loc="best")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel("sample size", fontsize=14)
    ax.set_ylabel("runtime [s]", fontsize=14)
    ax.set_title(f"{num_runs=}  &  {num_repetitions=}", fontsize=14)

    fig.tight_layout()

    return fig, ax


def get_runtimes(functions, sample_sizes, num_runs, num_repetitions, rng):
    time_function = time_average_runtime(
        num_runs=num_runs, num_repetitions=num_repetitions
    )

    output = collections.defaultdict(list)

    for size in sample_sizes:
        for func in functions:
            f = functools.partial(func, values=get_random_letters(size, rng))
            output[func.__name__].append(time_function(f))

    output["sample_sizes"] = sample_sizes

    return output


@curry
def time_average_runtime(func, num_runs, num_repetitions):
    total_runtime_per_repeat = tuple(
        timeit.Timer(func).repeat(repeat=num_repetitions, number=num_runs)
    )
    div_by_num_runs = curried.map(core.op(operator.truediv, y=num_runs))
    avg_runtime_per_repeat = div_by_num_runs(total_runtime_per_repeat)
    return statistics.mean(avg_runtime_per_repeat)


@curry
def time_min_runtime(func, num_runs, num_repetitions):
    total_runtime_per_repeat = tuple(
        timeit.Timer(func).repeat(repeat=num_repetitions, number=num_runs)
    )
    div_by_num_runs = curried.map(core.op(operator.truediv, y=num_runs))
    avg_runtime_per_repeat = div_by_num_runs(total_runtime_per_repeat)
    return min(avg_runtime_per_repeat)


def freq_pd(values):
    return pd.DataFrame(core.freq(values))


def enhanced_value_counts(values):
    """Equivalent Pandas implementation of freq."""
    s = pd.Series(values).value_counts(
        sort=True,
        ascending=False,
        bins=None,
        dropna=False,
    )

    df = pd.DataFrame(s, columns=["n"])
    df["N"] = df["n"].cumsum()
    df["r"] = df["n"] / df["n"].sum()
    df["R"] = df["r"].cumsum()

    return df


def get_random_letters(size, rng):
    return tuple(rng.choice(tuple(string.ascii_lowercase), size=size))


if __name__ == "__main__":
    main()
