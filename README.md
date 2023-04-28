<p align="center">
<img src="https://raw.githubusercontent.com/estripling/bumbag/main/docs/source/_static/logo.png" width="180" alt="The BumBag logo.">
</p>

<p align="center">
<a href="https://pypi.org/project/bumbag"><img alt="pypi" src="https://img.shields.io/pypi/v/bumbag"></a>
<a href="https://readthedocs.org/projects/bumbag/?badge=latest"><img alt="docs" src="https://readthedocs.org/projects/bumbag/badge/?version=latest"></a>
<a href="https://github.com/estripling/bumbag/actions/workflows/ci.yml"><img alt="ci status" src="https://github.com/estripling/bumbag/actions/workflows/ci.yml/badge.svg?branch=main"></a>
<a href="https://codecov.io/gh/estripling/bumbag"><img alt="coverage" src="https://codecov.io/github/estripling/bumbag/coverage.svg?branch=main"></a>
<a href="https://github.com/estripling/bumbag/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/pypi/l/bumbag"></a>
</p>

## About

BumBag is a collection of Python utility functions:

- [Documentation](https://bumbag.readthedocs.io/en/stable/index.html)
- [Example usage](https://bumbag.readthedocs.io/en/stable/example.html)
- [API Reference](https://bumbag.readthedocs.io/en/stable/autoapi/bumbag/index.html)

## Installation

`bumbag` is available on [PyPI](https://pypi.org/project/bumbag/) for Python 3.8+:

```shell
pip install bumbag
```

## Examples

Easily [`flatten`](https://bumbag.readthedocs.io/en/stable/autoapi/bumbag/index.html#bumbag.flatten) an irregular list:

```python
>>> import bumbag
>>> irregular_list = [
...     ["one", 2],
...     3,
...     [(4, "five")],
...     [[["six"]]],
...     "seven",
...     [],
... ]
>>> list(bumbag.flatten(irregular_list, 8, [9, ("ten",)]))
['one', 2, 3, 4, 'five', 'six', 'seven', 8, 9, 'ten']
```

Use [`highlight_string_differences`](https://bumbag.readthedocs.io/en/stable/autoapi/bumbag/index.html#bumbag.highlight_string_differences) to see differences between two strings easily:

```python
>>> import bumbag
>>> print(bumbag.highlight_string_differences("hello", "hall"))
hello
 |  |
hall
```

Quickly compare two Python sets with [`two_set_summary`](https://bumbag.readthedocs.io/en/stable/autoapi/bumbag/index.html#bumbag.two_set_summary):

```python
>>> import bumbag
>>> x = {"a", "c", "b", "g", "h"}
>>> y = {"c", "d", "e", "f", "g"}
>>> summary = bumbag.two_set_summary(x, y)
>>> print(summary["report"])
    x (n=5): {'a', 'b', 'c', ...}
    y (n=5): {'c', 'd', 'e', ...}
x | y (n=8): {'a', 'b', 'c', ...}
x & y (n=2): {'c', 'g'}
x - y (n=3): {'a', 'b', 'h'}
y - x (n=3): {'d', 'e', 'f'}
x ^ y (n=6): {'a', 'b', 'd', ...}
jaccard = 0.25
overlap = 0.4
dice = 0.4
disjoint?: False
x == y: False
x <= y: False
x <  y: False
y <= x: False
y <  x: False
```

## Contributing to BumBag

Your contribution is greatly appreciated!
See the following links to help you get started:

- [Contributing Guide](https://bumbag.readthedocs.io/en/latest/contributing.html)
- [Developer Guide](https://bumbag.readthedocs.io/en/latest/developers.html)
- [Contributor Code of Conduct](https://bumbag.readthedocs.io/en/latest/conduct.html)

## License

`bumbag` was created by the BumBag Developers.
It is licensed under the terms of the BSD 3-Clause license.
