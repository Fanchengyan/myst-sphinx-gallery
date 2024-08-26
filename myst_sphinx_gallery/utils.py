from __future__ import annotations

import warnings
from functools import wraps
from pathlib import Path
from typing import Literal


def ensure_dir_exists(dir_path: Path) -> None:
    """Ensure that the directory exists.

    dir_path : Path
        The path to the directory.
    """
    if not dir_path.exists():
        dir_path.mkdir(parents=True)


def safe_remove_file(file: Path) -> None:
    """Remove a file if it exists."""
    if file.exists():
        file.unlink()


def abs_path(
    path: Path | str,
    root_dir: Path | str,
    method: Literal["resolve", "rglob"] = "resolve",
) -> Path:
    """Convert a relative path to an absolute path.

    Parameters
    ----------
    path : Path | str
        The relative path.
    root_dir : Path | str
        The root directory.
    method : Literal["resolve", "rglob"], optional
        The method to use for converting the path, by default "resolve".

        - resolve: Use the ``resolve`` method of the Path class to convert the path.
        - rglob: try to find a matched path in the root directory using ``rglob``.

    Returns
    -------
    Path
        The absolute path.

    """
    path = str(Path(path).as_posix())
    if method == "resolve":
        if path.startswith("/"):
            path = f".{path}"
        return (Path(root_dir) / path).resolve()
    elif method == "rglob":
        path = Path(path).name
        files = list(Path(root_dir).rglob(path))
        if len(files) == 0:
            msg = f"No file found for {path} in {root_dir}"
            raise FileNotFoundError(msg)
        elif len(files) > 1:
            msg = (
                f"Multiple files found for {path} in {root_dir}"
                "first one will be used."
            )
            warnings.warn(msg, stacklevel=2)
        return files[0]
    else:
        raise ValueError(f"Invalid method: {method}")


def file_in_folder(file_path: Path | str, folder_path: Path | str) -> bool:
    """Check if the file is in the folder.

    Subdirectories are also considered.

    Parameters
    ----------
    file_path : Path | str
        The path to the file.
    folder_path : Path | str
        The path to the folder.

    Returns
    -------
    bool
        True if the file is in the folder, False otherwise.

    """
    folder_path = Path(folder_path)
    file_path = Path(file_path)
    return len(list(folder_path.rglob(file_path.name))) > 0


def print_run_time(func):
    """Print the run time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        import time

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print(f"Run time for {func.__name__}: {end_time - start_time:.2f} seconds")

        return result

    return wrapper


def gallery_static_path() -> Path:
    """Return the path to the CSS file."""
    return Path(__file__).parent / "_static"


def default_thumbnail() -> Path:
    """Return the path to the default thumbnail image."""
    return gallery_static_path() / "no_image.png"
