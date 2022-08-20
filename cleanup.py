"""A script to clean up Python cache files and directories."""

from pathlib import Path
from shutil import rmtree


def main():
    pwd = Path(".")
    file_extensions = ["*.py[co]", ".coverage", ".coverage.*"]
    directories = ["__pycache__", ".pytest_cache", ".ipynb_checkpoints"]

    for file_extension in file_extensions:
        for path in pwd.rglob(file_extension):
            print(f"deleting {path}")
            path.unlink()

    for directory in directories:
        for path in pwd.rglob(directory):
            print(f"deleting {path}")
            rmtree(path.absolute(), ignore_errors=False)


if __name__ == "__main__":
    main()
