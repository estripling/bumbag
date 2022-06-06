# BumBag

[![pypi](https://img.shields.io/pypi/v/bumbag)](https://pypi.org/project/bumbag)
[![python](https://img.shields.io/badge/python-%5E3.8-blue)](https://pypi.org/project/bumbag)
[![license](https://img.shields.io/pypi/l/bumbag)](https://github.com/estripling/bumbag/blob/main/LICENSE)
[![ci status](https://github.com/estripling/bumbag/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/estripling/bumbag/actions/workflows/ci.yml)
[![docs](https://readthedocs.org/projects/bumbag/badge/?version=latest)](https://readthedocs.org/projects/bumbag/?badge=latest)
[![coverage](https://codecov.io/github/estripling/bumbag/coverage.svg?branch=main)](https://codecov.io/gh/estripling/bumbag)
[![downloads](https://pepy.tech/badge/bumbag)](https://pepy.tech/project/bumbag)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1&labelColor=ef8336)](https://pycqa.github.io/isort/)

## About

A package for Python utility functions.

What is this package about?
Is its aim to offer functionality like a multi-tool pocketknife?
Or like the utility belt of a caped crusader?
Well, the purpose of a bumbag is to put in all the things you need often!
As such, the BumBag package is a collection of frequently used Python functions.

## Dictionary definition

bumbag `/ˈbʌmbæg/` (*noun countable*) -
a small bag attached to a long strap that you fasten around your waist to keep money, keys, and other small things in.

## Installation

`bumbag` is available on [PyPI](https://pypi.org/project/bumbag/):

```bash
pip install bumbag
```

## Usage

Quickly compare two Python sets with [`two_set_summary`](https://bumbag.readthedocs.io/en/stable/autoapi/bumbag/math/index.html#bumbag.math.two_set_summary):

```python
from bumbag.math import two_set_summary

x = {"a", "c", "b", "g", "h"}
y = {"c", "d", "e", "f", "g"}
summary = two_set_summary(x, y)
print(summary["report"])
```

```text
    x (n=5): {'a', 'b', 'c', ...}
    y (n=5): {'c', 'd', 'e', ...}
x | y (n=8): {'a', 'b', 'c', ...}
x & y (n=2): {'c', 'g'}
x - y (n=3): {'a', 'b', 'h'}
y - x (n=3): {'d', 'e', 'f'}
x ^ y (n=6): {'a', 'b', 'd', ...}
jaccard = 0.25
overlap = 0.4
disjoint?: False
x == y: False
x <= y: False
x <  y: False
y <= x: False
y <  x: False
```

Don't forget to check out [more examples](https://bumbag.readthedocs.io/en/stable/example.html#) and the [API Reference](https://bumbag.readthedocs.io/en/stable/autoapi/index.html).


## Contributing

Have you ever caught yourself thinking: "Ahh ... I need *that function* again. I have to copy it from another project."?
If you have, why not sharing your awesome utility function with the rest of the world?

To do so, check out the [contributing guidelines](https://bumbag.readthedocs.io/en/latest/contributing.html) and the [guide for developer](https://bumbag.readthedocs.io/en/latest/developers.html).
Please note that this project is released with a [Code of Conduct](https://bumbag.readthedocs.io/en/latest/conduct.html).
By contributing to this project, you agree to abide by its terms.

## License

`bumbag` was created by BumBag Developers.
It is licensed under the terms of the BSD 3-Clause license.

## Credits

`bumbag` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the [`pypkgcookiecutter` template](https://github.com/estripling/pypkgcookiecutter).
