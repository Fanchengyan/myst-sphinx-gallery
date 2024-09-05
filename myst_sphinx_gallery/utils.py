"""Utility functions for the myst-sphinx-gallery package."""

from __future__ import annotations

import re
import shutil
import warnings
from functools import wraps
from pathlib import Path
from typing import Literal

import nbformat


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


def safe_remove_dir(dir_path: Path) -> None:
    """Remove a directory if it exists."""
    if dir_path.exists():
        shutil.rmtree(dir_path)


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
    if method == "rglob":
        path = Path(path).name
        files = list(Path(root_dir).rglob(path))
        if len(files) == 0:
            msg = f"No file found for {path} in {root_dir}"
            raise FileNotFoundError(msg)
        if len(files) > 1:
            msg = (
                f"Multiple files found for {path} in {root_dir}"
                "first one will be used."
            )
            warnings.warn(msg, stacklevel=2)
        return files[0]
    msg = f"Invalid method: {method}"
    raise ValueError(msg)


def parse_files_without_suffix(path: Path | str) -> set[Path]:
    """Parse the files without the suffix.

    Support wildcard in the path name to match multiple files.

    Parameters
    ----------
    path : Path | str
        The path without the suffix.

    """
    path = Path(path)
    if not path.parent.exists():
        msg = f"Directory not found: {path.parent}. Please check the path."
        raise FileNotFoundError(msg)

    pattern = path.name if "*" in path.name else f"{path.name}.*"
    files = set(path.parent.glob(pattern))

    if len(files) == 0:
        msg = f"No file found for {pattern} in {path.parent}"
        raise FileNotFoundError(msg)
    return files


def get_rst_title(
    file_path: Path | str | None = None, content: str | None = None
) -> str | None:
    """Get the title of a reStructuredText file.

    Either the file path or the content of the file should be provided.

    Parameters
    ----------
    file_path : Path, optional
        The path to the reStructuredText file, by default None.
    content : str, optional
        The content of the reStructuredText file, by default None.
        If not provided, the content is read from the file.

    """
    if file_path is None and content is None:
        msg = "Either file_path or content should be provided."
        raise ValueError(msg)
    if content is None:
        with open(file_path, encoding="utf-8") as file:  # noqa: PTH123
            content = file.read()

    lines = content.splitlines()
    title = ""

    for i, line in enumerate(lines):
        line_content = line.strip()
        if title == "":
            if not _is_rst_title_line(line_content):
                continue
            title_lines_cdt = [line_content]
            if i > 0:
                title_lines_cdt.insert(0, lines[i - 1])
            if i < len(lines) - 1:
                title_lines_cdt.append(lines[i + 1])
            title, _ = _parse_rst_title(title_lines_cdt)
            continue
    return title


def extract_title_and_tooltip(file_path: Path | str) -> tuple[str, str]:
    """Extract the title and tooltip from a file.

    The file can be either a reStructuredText or a markdown/notebook file.

    Parameters
    ----------
    file_path : Path
        The path to the file.

    Returns
    -------
    title, tooltip : str, str
        The title and tooltip in the string format.

    """
    file_path = Path(file_path)
    suffix = file_path.suffix

    if suffix in [".rst", ".md"]:
        content = file_path.read_text(encoding="utf-8")
        if file_path.suffix == ".rst":
            title, tooltip = _extract_rst_title_and_tooltip(content)
        elif file_path.suffix == ".md":
            title, tooltip = _extract_md_title_and_tooltip(content)
    elif file_path.suffix == ".ipynb":
        content = load_nb_markdown(file_path)
        title, tooltip = _extract_md_title_and_tooltip(content)
    else:
        msg = f"Invalid file extension: {file_path.suffix}"
        raise ValueError(msg)
    return title, tooltip


def _extract_md_title_and_tooltip(content: str) -> list[str, str]:
    r"""Extract the title and tooltip from the markdown content.

    The first paragraph is considered as the tooltip.

    Returns
    -------
    title, tooltip : str, str
        The title and tooltip in the string format. The ``\n`` characters will be
        removed from the tooltip automatically.

    """
    lines = content.splitlines()
    title = ""
    tooltip = []

    for line in lines:
        line_content = line.strip()
        if not title:
            if not line_content.startswith("# "):
                continue
            title = line_content[2:].strip()
            continue
        if line_content:
            tooltip.append(line_content)
        if len(tooltip) > 0 and not line_content:
            break

    return title, " ".join(tooltip)


def _extract_rst_title_and_tooltip(content: str) -> list[str, str]:
    """Extract the title and tooltip from the reStructuredText content.

    The first paragraph is considered as the tooltip.

    Returns
    -------
    title, tooltip : str, str
        The title and tooltip in the string format.

    """
    lines = content.splitlines()
    title = ""
    tooltip = []

    for i, line in enumerate(lines):
        line_content = line.strip()
        if title == "":
            if not _is_rst_title_line(line_content):
                continue
            title_lines_cdt = [line_content]
            if i > 0:
                title_lines_cdt.insert(0, lines[i - 1])
            if i < len(lines) - 1:
                title_lines_cdt.append(lines[i + 1])
            title, title_lines = _parse_rst_title(title_lines_cdt)
            continue
        if line_content in title_lines:
            continue
        if line_content:
            tooltip.append(line_content)
        if len(tooltip) > 0 and not line_content:
            break

    return title, " ".join(tooltip)


def _is_rst_title_line(line: str) -> bool:
    line_chars = set(line.strip())
    return bool(len(line_chars) == 1 and line_chars.pop() in ["-", "="])


def _parse_rst_title(lines: list[str]) -> str:
    """Parse the title from the rst content.

    Parameters
    ----------
    lines : list[str]
        The candidate lines for the title.

    Returns
    -------
    title: str
        The title of the rst content.
    title_lines: list[str]
        The lines containing the title.

    """
    title_candidates = []
    title_sign_len = None
    for line in lines:
        line = line.strip()  # noqa: PLW2901
        line_chars = set(line)
        if len(line_chars) == 1 and line_chars.pop() in ["-", "="]:
            title_sign_len = len(line)
            title_sign_line = line
            continue
        title_candidates.append(line)

    if len(title_candidates) == 0 or title_sign_len is None:
        msg = "No title line found."
        warnings.warn(msg, stacklevel=2)
        return "", []

    title_list = [line for line in title_candidates if len(line) == title_sign_len]
    if len(title_list) > 1:
        msg = "Multiple title lines found."
        warnings.warn(msg, stacklevel=2)
    title = title_list[0]
    return title, [title, title_sign_line]


def get_base_gallery_items(
    content: str,
    style: Literal["rst", "md"] = "rst",
) -> list[str]:
    """Get the sub-gallery items from the given content.

    Parameters
    ----------
    content : str
        The reStructuredText content.
    style : Literal["rst", "md"], optional
        The style of the content, by default "rst".

    Returns
    -------
    items : list[str]
        The items in the sub-gallery.

    """
    if style == "rst":
        base_gallery_directives = _get_rst_base_gallery_directives(content)
    elif style == "md":
        base_gallery_directives = _get_md_base_gallery_directives(content)
    else:
        msg = f"Invalid style: {style}"
        raise ValueError(msg)

    items = []
    for directive in base_gallery_directives:
        items.extend(_get_base_gallery_items(directive))
    return items


def _get_base_gallery_items(content: str) -> list[str]:
    """Extract items from the content, ensuring only indented items are matched.

    This function is used to extract items from only contain a base-gallery
    directive.

    Returns
    -------
    options : dict[str, str]
        The options in the base-gallery directive.
    items : list[str]
        The items in the base-gallery.

    """
    lines = content.split("\n")

    items = []
    for line in lines:
        stripped_line = line.strip()
        if (
            stripped_line.startswith((":", "```"))
            or ".. base-gallery::" in stripped_line
        ):
            continue
        if stripped_line:
            items.append(stripped_line)
    return items


def _get_rst_base_gallery_directives(content: str) -> list[str]:
    """Get the sub-gallery directives from the rst content.

    If multiple sub-gallery directives are found, all of them are returned.
    """
    lines = content.expandtabs(4).splitlines()
    gallery_list = []
    idx = 0
    is_base_gallery = False
    is_other_directive = False
    other_directive_num_spaces = 0
    gallery_num_spaces = 0
    for line in lines:
        num_spaces = len(line) - len(line.lstrip())
        # skip other directives, to avoid parsing base gallery inside them
        if line.strip().startswith("..") and not line.strip().startswith(
            ".. base-gallery::"
        ):
            other_directive_num_spaces = num_spaces
            is_other_directive = True
            continue
        if is_other_directive:
            if num_spaces <= other_directive_num_spaces and line.strip() != "":
                is_other_directive = False
            else:
                continue
        # start of the gallery
        if line.strip().startswith(".. base-gallery::"):
            gallery_num_spaces = num_spaces
            is_base_gallery = True
            gallery_list.append([line[num_spaces:]])
        elif is_base_gallery:
            #  end of the gallery, reset flags
            if num_spaces <= gallery_num_spaces and line.strip() != "":
                is_base_gallery = False
                other_directive_num_spaces = 0
                idx += 1
            else:
                gallery_list[idx].append(line[gallery_num_spaces:])

    return ["\n".join(gallery).strip() for gallery in gallery_list]


def _get_md_num_directive_signs(line: str) -> int:
    """Get the number of directive signs in the line for markdown content."""
    line = line.strip()
    if line.startswith("```"):
        return len(line) - len(line.lstrip("`"))
    if line.startswith(":::"):
        return len(line) - len(line.lstrip(":"))
    return 0


def _is_md_directive_start(line: str) -> bool:
    """Check if the line is a directive start in markdown content."""
    line = line.strip()
    return line.startswith(("```", ":::")) and "{" in line


def _get_md_base_gallery_directives(content: str) -> list[str]:
    """Get the sub-gallery directives from the markdown content.

    If multiple sub-gallery directives are found, all of them are returned.
    """
    lines = content.expandtabs(4).splitlines()
    gallery_list = []
    idx = 0
    is_base_gallery = False
    is_other_directive = False
    num_other_directive_signs = 0
    for line in lines:
        line = line.strip()  # noqa: PLW2901
        num_directive_signs = _get_md_num_directive_signs(line)
        # skip other directives, to avoid parsing base gallery inside them
        if is_other_directive:
            if (
                line.startswith(("```", ":::"))
                and num_directive_signs == num_other_directive_signs
            ):
                is_other_directive = False
            continue
        if _is_md_directive_start(line) and "base-gallery" not in line:
            is_other_directive = True
            num_other_directive_signs = num_directive_signs
            continue

        # start of the base gallery
        if line.startswith(("```{base-gallery}", ":::{base-gallery}")):
            is_base_gallery = True
            gallery_list.append([line])
        elif is_base_gallery:
            if line.startswith(("```", ":::")):
                gallery_list[idx].append(line)
                is_base_gallery = False
                idx += 1
            else:
                gallery_list[idx].append(line)

    return ["\n".join(gallery).strip() for gallery in gallery_list]


def to_section_title(title: str) -> str:
    """Convert a title to a reStructuredText section title."""
    header_line = "-" * len(title)
    return f"\n\n{title}\n{header_line}\n"


def remove_num_prefix(header_file: Path) -> tuple[str, str]:
    """Remove the number prefix from the example file/dir."""
    folder, name = header_file.parent.stem, header_file.name
    if folder.split("-")[0].isdigit():
        folder = "-".join(folder.split("-")[1:])
    if name.split("-")[0].isdigit():
        name = "-".join(name.split("-")[1:])
    return folder, name


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


def print_run_time(func: callable) -> callable:
    """Print the run time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        import time

        time.time()
        result = func(*args, **kwargs)
        time.time()

        return result

    return wrapper


def load_nb_markdown(nb_file: Path) -> str:
    """Load the markdown content from a Jupyter notebook file as string."""
    with Path(nb_file).open(encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    markdown_cells = [
        cell.source for cell in notebook.cells if cell.cell_type == "markdown"
    ]
    return "\n".join(markdown_cells)


def gallery_static_path() -> Path:
    """Return the path to the CSS file."""
    return Path(__file__).parent / "_static"


def default_thumbnail() -> Path:
    """Return the path to the default thumbnail image."""
    return gallery_static_path() / "no_image.png"


def remove_special_chars(input_string: str) -> str:
    """Remove special characters from a string.

    Special characters are typically are used for styling content. This function
    is useful for removing special characters from the title and tooltip.
    """
    return re.sub(r"[^a-zA-Z0-9|:.,?!_ -]+", "", input_string)
