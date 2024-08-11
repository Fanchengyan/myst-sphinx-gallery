from __future__ import annotations

from pathlib import Path


def ensure_dir_exists(dir_path: Path) -> None:
    """Ensure that the directory exists.

    dir_path : Path
        The path to the directory.
    """
    if not dir_path.exists():
        dir_path.mkdir(parents=True)


def safe_remove_file(file: Path):
    """Remove a file if it exists."""
    if file.exists():
        file.unlink()


def abs_path(path: Path | str, root_dir: Path | str) -> Path:
    """Convert a relative path to an absolute path."""
    path = str(Path(path).as_posix())
    if path.startswith("/"):
        path = f".{path}"
    return (Path(root_dir) / path).resolve()
