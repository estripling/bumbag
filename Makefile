SHELL := /bin/zsh
PYTHON := python3
POETRY := poetry

.PHONY: help \
	check \
	check_style \
	run_tests \
	clean \
	create_docs \
	remove_docs \
	build_package \
	publish_to_test_pypi \
	publish_to_pypi

## help                                 :: print this help
help: Makefile
	@sed -n 's/^##//p' $<

## check                                :: run all checks using check_style, run_tests, and clean
check: clean check_style run_tests clean

## check_style                          :: check code style with isort, black, and flake8
check_style:
	$(PYTHON) -m isort ./
	@echo "\n"
	$(PYTHON) -m black ./
	@echo "\n"
	$(PYTHON) -m flake8 ./
	@echo "\n"

## run_tests                            :: run pytest with coverage report
run_tests:
	$(PYTHON) -m pytest --doctest-modules src/
	@echo "\n"
	$(PYTHON) -m pytest --cov=src/ tests/
	@echo "\n"

## clean                                :: remove Python cache files and directories
clean:
	$(PYTHON) scripts/cleanup.py
	@echo "\n"

## create_docs                          :: create local documentation files
create_docs:
	cd docs; make html; cd ..;

## remove_docs                          :: remove local documentation files
remove_docs:
	@rm -rf docs/_build/

## build_package                        :: build sdist and wheel distributions
build_package:
	$(POETRY) build

## publish_to_test_pypi                 :: publish to TestPyPI
publish_to_test_pypi:
	$(POETRY) config repositories.test-pypi https://test.pypi.org/legacy/
	$(POETRY) publish -r test-pypi

## publish_to_pypi                      :: publish to PyPI
publish_to_pypi:
	$(POETRY) publish
