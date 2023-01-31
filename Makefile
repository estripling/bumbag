SHELL := /bin/zsh
PYTHON := python3
POETRY := poetry

.PHONY: help \
	check \
	check-style \
	run-tests \
	clean \
	create-docs \
	remove-docs \
	remove-local-branches \
	build-package \
	publish-to-test-pypi \
	publish-to-pypi

## commands
##  - help                                 :: print this help
help: Makefile
	@sed -n 's/^##//p' $<

##  - check                                :: check style, run tests, and clean up cache all at once
check: clean check-style run-tests clean

##  - check-style                          :: check code style with isort, black, and flake8
check-style:
	$(PYTHON) -m isort ./
	@echo "\n"
	$(PYTHON) -m black ./
	@echo "\n"
	$(PYTHON) -m flake8 ./
	@echo "\n"

##  - run-tests                            :: run pytest with coverage report
run-tests:
	$(PYTHON) -m pytest
	@echo "\n"

##  - clean                                :: remove Python cache files and directories
clean:
	$(PYTHON) scripts/cleanup.py
	@echo "\n"

##  - create-docs                          :: create local documentation files
create-docs:
	cd docs; make html; cd ..;

##  - remove-docs                          :: remove local documentation files
remove-docs:
	@rm -rf docs/_build/

##  - remove-local-branches                :: git remove local branches, except main
remove-local-branches:
	git -P branch | grep -v "main" | grep -v \* | xargs git branch -D

##  - build-package                        :: build sdist and wheel distributions
build-package:
	$(POETRY) build

##  - publish-to-test-pypi                 :: publish to TestPyPI
publish-to-test-pypi:
	$(POETRY) config repositories.test-pypi https://test.pypi.org/legacy/
	$(POETRY) publish -r test-pypi

##  - publish-to-pypi                      :: publish to PyPI
publish-to-pypi:
	$(POETRY) publish
