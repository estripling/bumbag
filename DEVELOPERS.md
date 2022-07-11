# Developer Guide

## Development Setup

It is assumed the following software packages are installed on your system:

* [Git](https://git-scm.com/)
* [Conda](https://docs.conda.io/en/latest/)
* [Poetry](https://python-poetry.org/)

In root directory, run the following commands if your system supports [GNU Make](https://www.gnu.org/software/make/):

```console
make create_env
conda activate <pkg-env>
make install
```

If your system does not support GNU Make, run the corresponding commands manually.

## Test

In root directory, execute the following command to run all tests:

```console
make test
```

## Code Style

In root directory, run the following command to check code style:

```console
make check_style
```

## Git Commit Guidelines

The commit style of BumBag is the [Angular style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines), but used as suggested in this [Git commit messages guide](https://py-pkgs.org/07-releasing-versioning#automatic-version-bumping).

### Commit Message Format

Each commit message consists of a **header**, a **body** and a **footer**.
The header has a special format that includes a **type**, a **scope**, and a **subject**:

```text
<type>(<scope>): <subject>

(<body>: explains motivation for the change)

(<footer>: note BREAKING CHANGES here, and issues to be closed)
```

The **header** is mandatory but the **scope** of the header is optional.
The **subject** is a short summary in present tense.

Any line of the commit message cannot be longer than 100 characters!
This allows the message to be easier to read on GitHub as well as in various git tools.

### Revert

If the commit reverts a previous commit, it should begin with `revert:`, followed by the header
of the reverted commit.
In the body it should say: `This reverts commit <hash>.`, where the hash is the SHA of the commit
being reverted.

### Type

Must be one of the following:

* **feat**: A new feature.
* **fix**: A bug fix.
* **docs**: Documentation changes.
* **style**: Changes that do not affect the meaning of the code (whitespace, formatting, missing comma).
* **refactor**: A code change that neither fixes a bug nor adds a feature.
* **perf**: A code change that improves performance.
* **test**: Changes to the test framework, i.e., adding missing or correcting existing tests.
* **build**: Changes to the build process or tools.

### Scope

The scope is an optional keyword that provides context for where the change was made.
It can be anything relevant to your package or development workflow (e.g., it could be the module or function name affected by the change).

You can use `*` when the change affects more than a single scope.

### Subject

The subject contains succinct description of the change:

* Use the imperative, present tense: "change" not "changed" nor "changes".
* Do not capitalize first letter.
* No period (.) at the end.

### Body

Just as in the **subject**, use the imperative, present tense: "change" not "changed" nor "changes".
The body should include the motivation for the change and contrast this with previous behavior.

### Footer

The footer should contain any information about **Breaking Changes** and is also the place to
[reference GitHub issues that this commit closes](https://help.github.com/articles/closing-issues-via-commit-messages/).

**Breaking Changes** should start with the word `BREAKING CHANGE:` with a space or two newlines.
The rest of the commit message is then used for this.

## Docstring Guidelines

### General

General docstring convention in Python is described in [Python Enhancement Proposal (PEP) 257 — Docstring Conventions](https://www.python.org/dev/peps/pep-0257/), but there is flexibility in how you write your docstrings ([source](https://py-pkgs.org/03-how-to-package-a-python#writing-docstrings)).
A minimal docstring contains a single line describing what the object does, and that might be sufficient for a simple function or for when your code is in the early stages of development.
However, for code you intend to share with others (including your future self) a more comprehensive docstring should be written.
A typical docstring will include:

1. A one-line summary that does not use variable names or the function name.
2. An extended description.
3. Parameter types and descriptions.
4. Returned value types and descriptions.
5. Example usage.
6. Potentially more.

### Docstring Guidelines

There are different docstring styles available:

* [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard)
* [Google](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
* [sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html#the-sphinx-docstring-format)
* [DM Python Style Guide](https://developer.lsst.io/python/style.html#)

This package uses the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard) style, because it is readable, commonly used, and supported by [sphinx](https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html).
In the numpydoc style:

* Section headers are denoted as text underlined with dashes:
  ```text
  Parameters
  ----------
  ```

* Input arguments are denoted as:
  ```text
  name : type
      Description of parameter `name`.
  ```

* Output values use the same syntax above, but specifying the `name` is optional.
  ```text
  Returns
  -------
  int
      Description of anonymous integer return value.
  ```

  If both the name and type are specified, the Returns section takes the same form as the Parameters section:
  ```text
  Returns
  -------
  err_code : int
      Non-zero value indicates error code, or zero on success.
  err_msg : str or None
      Human readable error message, or None on success.
  ```

### Examples:

```python
def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.

    The one-line summary immediately follows the triple double quotes
    and ends with a dot. There is no blank line before the closing triple
    double quotes.

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    return param1 == int(param2)
```
