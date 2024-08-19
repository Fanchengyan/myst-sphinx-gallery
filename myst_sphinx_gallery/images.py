"""
A module to manage images in a MyST markdown/notebook/rst file.
"""

from __future__ import annotations

import base64
import io
import re
from pathlib import Path
from typing import Literal

import nbformat
from PIL import Image, ImageOps

from .utils import ensure_dir_exists, print_run_time

OperationMap = {
    "contain": ImageOps.contain,
    "cover": ImageOps.cover,
    "fit": ImageOps.fit,
    "pad": ImageOps.pad,
}
SaveKwargs = {
    "format": "WebP",
    "lossless": False,
    "compression": 6,
}


class Thumbnail:
    """A class to manage the thumbnail image"""

    _path: Path
    _image: Image.Image

    def __init__(
        self,
        image: Path | str | Image.Image,
        output_dir: Path | str,
        ref_size: tuple[int, int] | int = (320, 224),
        operation: Literal["thumbnail", "contain", "cover", "fit", "pad"] = "pad",
        max_animation_frames=50,
        quality_static: int = 80,
        quality_animated: int = 15,
        operation_kwargs: dict[str, int] | None = None,
        save_kwargs: dict[str, int] | None = None,
    ) -> None:
        """Initialize the Thumbnail object.

        path : Path | str | Image.Image
            The path to the thumbnail image, or the PIL image object.
        output_dir : Path
            The directory to save the thumbnail image.
        ref_size : tuple[int, int]
            the reference size of the thumbnail image for output.
        operation : str
            The operation to perform on the image. See the Pillow documentation
            for more information: `<https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#relative-resizing>`_
        max_animation_frames : int
            The maximum number of frames to extract from an animated image.
            If the image has more frames, will sample the frames uniformly.
        quality_static : int
            The quality of the static image thumbnail.
        quality_animated : int
            The quality of the animated image thumbnail.
        operation_kwargs : dict
            The keyword arguments for the operation.
        save_kwargs : dict
            The keyword arguments for the save method.
        """
        if operation_kwargs is None:
            operation_kwargs = {}
        if save_kwargs is None:
            save_kwargs = {}
        if isinstance(image, Image.Image):
            self._image = image
            if hasattr(image, "path"):
                self._path = Path(image.path)
            else:
                self._path = Path("no_image.png")
        elif isinstance(image, (str, Path)):
            self._path = Path(image)
            self._image = Image.open(image)
        else:
            raise ValueError("image must be a path or PIL Image object")

        self.operation = operation
        self.operation_kwargs = operation_kwargs
        self._output_dir = Path(output_dir)
        self.max_animation_frames = max_animation_frames
        self.quality_static = quality_static
        self.quality_animated = quality_animated

        self._ref_size = self._format_size(ref_size)
        self._save_kwargs = self._format_save_kwargs(save_kwargs)

    def __str__(self) -> str:
        return f"Thumbnail(path={self.path})"

    def __repr__(self) -> str:
        return f"Thumbnail(path={self.path})"

    def _format_save_kwargs(self, save_kwargs: dict) -> dict:
        """Format the save keyword arguments."""
        if not isinstance(save_kwargs, dict):
            raise ValueError("save_kwargs must be a dictionary")
        kwargs = SaveKwargs.copy()
        if self.image.n_frames > 1:
            kwargs.update(
                {
                    "quality": self.quality_animated,
                    "save_all": True,
                    "loop": 0,
                }
            )
        else:
            kwargs.update({"quality": self.quality_static})
        if self.operation == "pad":
            kwargs.update({"color": "00000000"})  # transparent background

        kwargs.update(save_kwargs)
        return kwargs

    def _parse_frames(self):
        """Parse the frames and duration of the output animated image."""
        n_frames = self.image.n_frames
        max_frames = self.max_animation_frames
        if n_frames > max_frames:
            interval = n_frames // max_frames
            frames = list(range(0, n_frames, interval))[:max_frames]
            duration = self.image.info["duration"] * interval
        else:
            frames = range(n_frames)
            duration = self.image.info["duration"]

        return frames, duration

    def _format_size(self, size: tuple[int, int] | int) -> tuple[int, int]:
        """Format the size of the thumbnail image to a tuple of length 2."""
        if isinstance(size, int):
            return size, size
        elif isinstance(size, tuple):
            if len(size) != 2:
                raise ValueError("size must be a tuple of length 2")
            return size
        else:
            try:
                size = tuple(size)
                if len(size) != 2:
                    raise ValueError("size must be a tuple of length 2")
                return size
            except Exception as e:
                if e is TypeError:
                    raise ValueError("size must be a tuple of length 2") from e

    @property
    def path(self) -> Path:
        """The path to the thumbnail image."""
        return self._path

    @property
    def output_dir(self) -> Path:
        """The directory to save the thumbnail image."""
        return self._output_dir

    @property
    def auto_output_path(self) -> Path:
        """Automatically generated output path for the thumbnail image."""
        out_file = self.output_dir / self.path.name
        return out_file.with_suffix(".thumbnail.webp")

    @property
    def image(self) -> Image.Image:
        """The thumbnail image."""
        return self._image

    @property
    def ref_size(self) -> tuple[int, int]:
        """The reference size of the thumbnail image."""
        return self._ref_size

    @property
    def save_kwargs(self) -> dict[str, int]:
        """The keyword arguments for the save method."""
        return self._save_kwargs

    def generate_thumbnail(self) -> Image.Image:
        """Generate the thumbnail image based on the operation."""
        if self.operation == "thumbnail":
            thumbnail = self.image.copy()
            thumbnail.thumbnail(self.ref_size)
            thumbnail.info.clear()
        else:
            operate = OperationMap[self.operation]
            image = self.image
            if self.operation == "pad":
                image = image.convert("RGBA")
            thumbnail = operate(image, self.ref_size, **self.operation_kwargs)

        return thumbnail

    @print_run_time
    def save_thumbnail(self, out_path: Path | None = None) -> Path:
        """Save the thumbnail image to the output directory.

        Parameters
        ----------
        out_path : Path
            The path to save the thumbnail image. If None, the image will be
            saved with the same name as the original image.

        Returns
        -------
        out_path : Path
            The path to the saved thumbnail image.
        """
        out_path = self.auto_output_path if out_path is None else Path(out_path)
        ensure_dir_exists(out_path.parent)
        print(f"Saving thumbnail to {out_path}")

        if self.image.n_frames > 1:
            frames_idx, duration = self._parse_frames()
            self.save_kwargs.update({"duration": duration})
            # extract frames
            frames = []
            for idx in frames_idx:
                self.image.seek(idx)
                frames.append(self.generate_thumbnail())

            frames[0].save(
                out_path,
                append_images=frames[1:],
                **self.save_kwargs,
            )
        else:
            thumbnail = self.generate_thumbnail()
            thumbnail.save(out_path, **self.save_kwargs)
        return out_path


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

    def __add__(self, other: DocImages) -> DocImages:
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
        with open(self.notebook_file, encoding="utf-8") as f:
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
        ensure_dir_exists(output_file.parent)
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

    with open(nb_file, encoding="utf-8") as f:
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


def strip_str(s: str) -> str:
    """Strip the string and remove quotes."""
    return s.strip().strip('"').strip("'").strip("`").strip()
