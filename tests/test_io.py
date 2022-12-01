import os
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

import bumbag as bb


@pytest.mark.parametrize("kind", ["zip", "gztar"])
def test_archive_files(kind):
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir).joinpath("test_file_for_archive_files.txt")

        with path.open("w") as fh:
            fh.write("Hello, World!\n")

        dir_path = Path(tmpdir).joinpath("test_directory_for_archive_files/")
        os.makedirs(dir_path)
        path2 = Path(dir_path).joinpath("test_file_for_archive_files2.txt")

        with path2.open("w") as fh:
            fh.write("Hello, Again!\n")

        bb.archive_files(target_dir=tmpdir, name="archive", kind=kind)

    if kind == "gztar":
        kind = "tar.gz"

    os.remove(f"archive.{kind}")


def test_lazy_read_lines():
    expected = ("one", "two", "three")

    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir).joinpath("test_file_for_lazy_read_lines.txt")

        with path.open("w") as fh:
            fh.write("\n".join(expected))

        actual = tuple(map(str.rstrip, bb.lazy_read_lines(path)))
        assert actual == expected

        for i, line in enumerate(bb.lazy_read_lines(str(path))):
            actual = line.replace("\n", "")
            assert actual == expected[i]

        with pytest.raises(FileNotFoundError):
            tuple(bb.lazy_read_lines(Path(tmpdir).joinpath("./not_exist.txt")))


class TestQueryYesNo:
    @pytest.mark.parametrize(
        "arg, answer, expected",
        [
            (None, "yes", True),
            (None, "no", False),
            ("yes", "yes", True),
            ("yes", "no", False),
            ("no", "yes", True),
            ("no", "no", False),
            ("yes", "\n", True),
            ("no", "\n", False),
        ],
    )
    def test_normal_usage(self, monkeypatch, arg, answer, expected):
        default = arg
        monkeypatch.setattr("sys.stdin", StringIO(answer))
        actual = bb.query_yes_no("Do you like BumBag?", default)
        assert actual == expected

    @pytest.mark.parametrize("arg", [1, "noo", "yeah"])
    def test_invalid_default_value(self, arg):
        default = arg
        with pytest.raises(ValueError):
            bb.query_yes_no("Do you like BumBag?", default)

    def test_subsequent_query(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("yay"))
        with pytest.raises(EOFError):
            bb.query_yes_no("Do you like BumBag?", "yes")
