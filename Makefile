# Global parameters
SHELL := /bin/bash
CONDA := conda
PYTHON := python
POETRY := poetry
PGK := bumbag
PGKENV := bumbag-py38
GHUSER := estripling


# https://peps.python.org/pep-0008/#maximum-line-length
MAXLINELENGTH := 79


# Main
.PHONY: all help program
all: program

help: Makefile
	@sed -n 's/^##//p' $<

program:
	@echo "use 'make help'"


## create_env :: Create env with conda
.PHONY: create_env
create_env:
	$(CONDA) create -n $(PGKENV) python=3.8


## remove_env :: Remove conda env
.PHONY: remove_env
remove_env:
	$(CONDA) env remove -n $(PGKENV)


## add_dev_dep :: Add main dev dependencies
.PHONY: add_dev_dep
add_dev_dep:
	$(POETRY) add --dev \
		pytest \
		pytest-cov \
		black \
		black[jupyter] \
		isort \
		flake8 \
		python-semantic-release


## add_dev_docs :: Add dev dependencies for documentation
.PHONY: add_dev_docs
add_dev_docs:
	$(POETRY) add --dev \
		jupyter \
		myst-nb \
		sphinx-autoapi \
		sphinx-rtd-theme \
		sphinx-copybutton


## add_dev_all :: Add all dev dependencies
.PHONY: add_dev_all
add_dev_all: add_dev_dep add_dev_docs


## install :: Install requirements in poetry.lock
.PHONY: install
install:
	$(POETRY) install


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


## echo_release_action :: Echo link to manually trigger release action
.PHONY: echo_release_action
echo_release_action:
	@echo https://github.com/$(GHUSER)/$(PGK)/actions/workflows/release.yml


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


## info :: Echo variables
.PHONY: info
info:
	@echo SHELL: $(SHELL)
	@echo PGK: $(PGK)
	@echo PGKENV: $(PGKENV)
	@echo GHUSER: $(GHUSER)
