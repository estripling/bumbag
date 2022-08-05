import os
import shutil
from datetime import datetime
from distutils.util import strtobool
from pathlib import Path
from tempfile import TemporaryDirectory


def archive_files(wildcards=None, target_dir=None, name=None, kind="zip"):
    """Archive files in target directory.

    Parameters
    ----------
    wildcards : None, list of str, default=None
        Specify a wildcard to archive files. If ``wildcards`` is None,
        all files in target directory are archived.
    target_dir : None, str, pathlib.Path, default=None
        Specify the target directory to archive. If ``target_dir`` is None,
        ``target_dir`` is set to be the current working directory.
    name : None, str, default=None
        Name of the archive. If ``name`` is None, archive name is the name of
        the target directory.
    kind : str, default="zip"
        Specify the archive type. Value is passed to the ``format`` argument of
        ``shutil.make_archive``, i.e., possible values are "zip", "tar",
        "gztar", "bztar", "xztar", or any other registered format.

    Returns
    -------
    NoneType
        Function has no return value. However, the archive of files of
        the target directory is stored in the current working directory.

    Examples
    --------
    >>> # Archive all Python files and Notebooks in current working directory
    >>> archive_files(["*.py", "*.ipynb"])  # doctest: +SKIP
    """
    wildcards = wildcards or ["**/*"]
    target_dir = target_dir or "."
    target_dir = Path(target_dir).resolve()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name = name or f"{timestamp}_{target_dir.stem}"

    with TemporaryDirectory() as tmpdir:
        for wildcard in wildcards:
            for src_file in target_dir.rglob(wildcard):
                if os.path.isdir(src_file):
                    os.makedirs(src_file, exist_ok=True)
                    continue

                dst_file = str(src_file).replace(str(target_dir), tmpdir)
                dst_dir = str(src_file.parent).replace(str(target_dir), tmpdir)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy(str(src_file), dst_file)

        shutil.make_archive(name, kind, tmpdir)


def query_yes_no(question, default=None):
    """Prompt user a yes/no question.

    Parameters
    ----------
    question: str
        Specify a yes/no question to prompt the user.
    default: None, str, default=None
        Define default answer:
         - If ``default`` is None, an explicit answer is needed from the user.
         - If ``default`` is "yes" or "no", the presumed answer, indicated by
           a capitial letter, is accepted when pressing <enter>.

    Returns
    -------
    bool
        ``True`` if user's answer is "yes" else ``False``.

    Raises
    ------
    ValueError
        If ``default`` is none of the following values: {None, "yes", "no"}.

    Examples
    --------
    >>> query_yes_no("Is all clear?")  # doctest: +SKIP
    Is all clear? [y/n] y<enter>
    True

    >>> query_yes_no("Do you like BumBag?", "yes")  # doctest: +SKIP
    Do you like BumBag? [Y/n] <enter>
    True

    >>> query_yes_no("Do you like BumBag?", "yes")  # doctest: +SKIP
    Do you like BumBag? [Y/n] yay<enter>
    Do you like BumBag? Please respond with 'yes' [Y] or 'no' [n] <enter>
    True
    """
    prompt = (
        "[y/n]"
        if default is None
        else "[Y/n]"
        if default == "yes"
        else "[y/N]"
        if default == "no"
        else "invalid"
    )

    if prompt == "invalid":
        raise ValueError(f"{default=} - must be either None, 'yes', or 'no'")

    answer = input(f"{question} {prompt} ").lower()

    while True:
        try:
            if answer == "" and default in ["yes", "no"]:
                return bool(strtobool(default))
            return bool(strtobool(answer))

        except ValueError:
            msg = "{} Please respond with 'yes' [{}] or 'no' [{}] ".format(
                question,
                "Y" if default == "yes" else "y",
                "N" if default == "no" else "n",
            )
            answer = input(msg).lower()
