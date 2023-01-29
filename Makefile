# Global parameters
SHELL := /bin/zsh
PYTHON := python3
POETRY := poetry
PGK := bumbag


# Using Black's default, as pandas-dev and scikit-learn
MAXLINELENGTH := 88


# Main
.PHONY: all help program
all: program

help: Makefile
	@sed -n 's/^##//p' $<

program:
	@echo "use 'make help'"


## test :: Run tests with coverage report
.PHONY: test
test: clean
	$(PYTHON) -m pytest --doctest-modules src/
	$(PYTHON) -m pytest --cov=$(PGK) tests/


## check_style :: Check code style
.PHONY: check_style
check_style: clean
	$(PYTHON) -m isort --line-length $(MAXLINELENGTH) --profile black ./
	$(PYTHON) -m black --line-length $(MAXLINELENGTH) ./
	$(PYTHON) -m flake8 --doctests --max-line-length $(MAXLINELENGTH) ./


## create_docs :: Create documentation source files with sphinx
.PHONY: create_docs
create_docs:
	cd docs; make html; cd ..;


## remove_docs_build :: Remove docs/_build/ directory (if there is a significant change)
.PHONY: remove_docs_build
remove_docs_build:
	rm -rf docs/_build/


## build_pkg :: Build sdist and wheel distributions
.PHONY: build_pkg
build_pkg:
	$(POETRY) build


## test_publish_pkg :: Publish to TestPyPI
.PHONY: test_publish_pkg
test_publish_pkg:
	$(POETRY) config repositories.test-pypi https://test.pypi.org/legacy/
	$(POETRY) publish -r test-pypi


## publish_pkg :: Publish to PyPI
.PHONY: publish_pkg
publish_pkg:
	$(POETRY) publish


## clean :: Clean up Python cache files and directories
.PHONY: clean
clean:
	$(PYTHON) cleanup.py
