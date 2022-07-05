from io import StringIO

import pytest

from bumbag import io


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
        actual = io.query_yes_no("Do you like BumBag?", default)
        assert actual == expected

    @pytest.mark.parametrize("arg", [1, "noo", "yeah"])
    def test_invalid_default_value(self, arg):
        default = arg
        with pytest.raises(ValueError):
            io.query_yes_no("Do you like BumBag?", default)

    def test_subsequent_query(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("yay"))
        with pytest.raises(EOFError):
            io.query_yes_no("Do you like BumBag?", "yes")
