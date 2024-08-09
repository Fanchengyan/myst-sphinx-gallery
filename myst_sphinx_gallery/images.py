"""
A module to manage images in a MyST markdown/notebook/rst file.
"""

from __future__ import annotations

import base64
import io
import re
from pathlib import Path

import nbformat
from PIL import Image


class DocImages:
    """A class to manage images in a MyST markdown/notebook/rst file."""

    _urls: list
    _alts: list
    _images: list[tuple[str, str]]

    def __init__(self, images: list[tuple[str, str]]) -> None:
        """Initialize the DocImages object.

        images : list[tuple[str, str]]
            A list of tuples, where each tuple contains the image url and alt text.
        """
        self._images = images
        self._urls, self._alts = self._parse_images()

    def __len__(self) -> int:
        """Return the number of images."""
        return len(self.images)

    def __str__(self) -> str:
        return f"DocImages(images={len(self.images)})"

    def __repr__(self) -> str:
        return f"DocImages(images={len(self.images)})"

    def __add__(self, other: "DocImages") -> "DocImages":
        if isinstance(other, DocImages):
            return DocImages(self.images + other.images)
        else:
            raise TypeError(
                f"unsupported operand type(s) for +: 'DocImages' and '{type(other)}'"
            )

    def __hash__(self) -> int:
        return hash(tuple(self.images))

    def __eq__(self, other: DocImages) -> bool:
        return self.images == other.images

    def __getitem__(self, idx: int) -> tuple[str]:
        """Return the image url at the specified index."""
        return self.images[idx][0]

    def _parse_images(self):
        """Parse the images urls and alt text."""
        if len(self.images) == 0:
            return [], []
        urls, alts = zip(*self.images)
        return urls, alts

    @property
    def images(self) -> list[tuple[str, str]]:
        """A list of tuples, where each tuple contains the image url and alt text."""
        return self._images

    @property
    def urls(self) -> list[str]:
        """A list of image urls."""
        return self._urls

    @property
    def alts(self) -> list[str]:
        """A list of image alt text."""
        return self._alts

    def where(self, alt: str) -> list[int]:
        """Return the indices of the images with the specified alt text."""
        return [i for i, a in enumerate(self.alts) if a == alt]

    def sel_urls(self, alt: str) -> list[str]:
        """Return the urls of the images with the specified alt text."""
        idx = self.where(alt)
        if len(idx) == 0:
            return []
        else:
            return [self.urls[i] for i in idx]


class CellImages:
    """A class to manage images in a notebook code cell output."""

    def __init__(
        self,
        notebook_file: Path,
    ) -> None:
        """Initialize the CellImages object."""
        self._notebook_file = Path(notebook_file)
        self._images = self._extract_images()

    def _extract_images(self):
        """Extract images from code cell outputs in a notebook."""
        with open(self.notebook_file, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        images = []
        for cell in notebook.cells:
            if cell.cell_type == "code":
                for output in cell.outputs:
                    if "data" in output and "image/png" in output.data:
                        # get base64 encoded image data
                        img_data = base64.b64decode(output.data["image/png"])
                        # convert to PIL image
                        img = Image.open(io.BytesIO(img_data))
                        images.append(img)
        return images

    def __len__(self) -> int:
        """Return the number of images."""
        return len(self.images)

    def __str__(self) -> str:
        return f"CellImages(images={len(self.images)})"

    def __repr__(self) -> str:
        return f"CellImages(images={len(self.images)})"

    @property
    def images(self) -> list[Image.Image]:
        """A list of images extracted from the notebook."""
        return self._images

    @property
    def notebook_file(self) -> Path:
        """The path to the notebook file."""
        return self._notebook_file

    def save_images(self, output_dir: Path):
        """Save the images to the output directory."""
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
        for i, img in enumerate(self.images):
            img.save(output_dir / f"{self.notebook_file.stem}_{i}.png")

    def save_image(self, output_file: Path, index: int):
        """Save an image to the output directory.

        Parameters
        ----------
        output_dir : Path
            The output directory.
        index : int
            The index of the image to save.
        """
        output_file = Path(output_file)
        _ensure_dir_exists(output_file.parent)
        img = self.images[index]
        img.save(output_file)


def parse_md_images(markdown_content: str) -> DocImages:
    """Parse the image information (url, alt) from a markdown content.

    Two types of markdown image syntax are supported:

    1. Conventional markdown image syntax: ``![alt](img/xxx.png)``
    2. Myst markdown image/figure syntax: See `Images and figures <https://myst-parser.readthedocs.io/en/latest/syntax/images_and_figures.html>`_ for more details.

    .. warning::

        The html image syntax is not supported.

    Parameters
    ----------
    markdown_content : str
        The markdown content.

    Returns
    -------
    images : DocImages
        A DocImages instance, which contains the image url and alt text.
    """
    images = []

    # case 1 (conventional markdown image syntax): ![alt](img/xxx.png)
    md_pattern = r"!\[(.*?)\]\((.*?)\)"
    for match in re.finditer(md_pattern, markdown_content):
        alt, url = match.groups()
        images.append((strip_str(url), strip_str(alt)))

    # case 2 (myst markdown image/figure syntax):
    myst_pattern = r"```\{(image|figure)\}\s+(.*?)\n(.*?)```"
    for match in re.finditer(myst_pattern, markdown_content, re.DOTALL):
        directive, url, options = match.groups()

        # find alt text
        alt_match = re.search(r":alt:\s*(.*?)\n", options)
        alt = alt_match.group(1).strip() if alt_match else ""

        images.append((strip_str(url), strip_str(alt)))

    return DocImages(images)


def load_nb_markdown(nb_file: Path) -> str:
    """Load the markdown content from a Jupyter notebook file."""

    with open(nb_file, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    markdown_cells = []
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            markdown_cells.append(cell.source)

    return "\n".join(markdown_cells)


def parse_rst_images(rst_content: str) -> DocImages:
    """Parse the images (url, alt) from a reStructuredText content.

    rst image/figure syntax are supported:

    .. code-block:: rst

        .. image:: xxx.png
               :alt: xxxx

        .. figure:: xxx.png
               :alt: xxxx

    Parameters
    ----------
    rst_content : str
        The reStructuredText content.

    Returns
    -------
    images : DocImages
        A DocImages instance, which contains the image url and alt text.
    """

    pattern = r"\.\.\s+(image|figure)::\s+(.*?)\n(?:\s+:.*?:\s*(.*?)\n)*"

    images = []
    for match in re.finditer(pattern, rst_content, re.DOTALL):
        url = match.group(2).strip()
        # find alt text
        alt_match = re.search(r":alt:\s*(.*?)\n", match.group(0))
        alt = alt_match.group(1).strip() if alt_match else ""
        images.append((strip_str(url), strip_str(alt)))

    return DocImages(images)


def _ensure_dir_exists(directory: Path):
    """Ensure that the directory exists."""
    if not directory.exists():
        directory.mkdir(parents=True)


def strip_str(s: str) -> str:
    """Strip the string and remove quotes."""
    return s.strip().strip('"').strip("'").strip("`").strip()
