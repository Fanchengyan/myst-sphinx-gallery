"""
A module for managing the gallery of examples.
"""

import warnings
from pathlib import Path
from typing import Literal

import nbformat
from docutils.core import publish_doctree
from docutils.nodes import title

from .images import CellImages, DocImages, parse_md_images, parse_rst_images
from .patterns import grid, grid_item_card, toc_gallery


class GalleryGenerator:
    """
    A class to generate the gallery for a folder.
    """

    def __init__(
        self,
        examples_dir: Path,
        gallery_dir: Path,
        thumb_strategy: Literal["first", "last"] = "first",
        thumb_strategy_notebook: Literal["code", "markdown"] = "code",
        default_thumb: Path | str = None,
    ) -> None:
        """Initialize the GalleryGenerator object.

        examples_dir: Path,
            The path to the input examples directory.
        gallery_dir : Path
            The path to the output gallery directory.
        thumb_strategy : Literal["first", "last"]
            The strategy for selecting the thumbnail image if multiple images
            are found in the example file.
        thumb_strategy_notebook : Literal["code", "markdown"]
            The strategy for selecting the thumbnail image if multiple images
            are found in the example file.
        default_thumb : Path | str
            The default thumbnail image to use if no image is found in the example
            file.
        """
        self.thumb_strategy = thumb_strategy
        self.thumb_strategy_notebook = thumb_strategy_notebook
        self.default_thumb = default_thumb

        self.examples_dir = Path(examples_dir).absolute()
        self.gallery_dir = Path(gallery_dir).absolute()

        self._scan_gallery_header_file()
        self._scan_example_folders()

        self.toc_str = ""
        self.grid_str = ""

    def _scan_gallery_header_file(self):
        """Scan header file for the whole gallery."""
        self._header_file = self.examples_dir / "GALLERY_HEADER.rst"
        if not self.header_file.exists():
            raise FileNotFoundError(
                f"Gallery header file not found: {self.header_file}"
            )

    def _scan_example_folders(self):
        """Scan the sub-folders that contain example files."""
        items = self.header_file.parent.glob("*")
        folders = []
        for item in items:
            if not item.is_dir():
                continue
            header_file = item / "GALLERY_HEADER.rst"
            if not header_file.exists():
                continue
            folders.append(item)
        if len(folders) == 0:
            warnings.warn(f"No valid subfolders found in {self.examples_dir}")
        self._folders = sorted(folders)

    @property
    def folders(self) -> list[Path]:
        """Folders that contain example files."""
        return self._folders

    @property
    def header_file(self) -> Path:
        """The path to the gallery header file."""
        return self._header_file

    @property
    def toc(self) -> str:
        """The table of contents for the gallery."""
        return toc_gallery + self.toc_str

    @property
    def grid(self) -> str:
        """The grid for the gallery."""
        return grid + self.grid_str

    def update_gallery_toc(self, section_index_file: str):
        """Update the gallery table of contents."""
        rel_path = section_index_file.relative_to(self.gallery_dir)
        self.toc_str += f"\n    {rel_path}"

    def update_gallery_grid(self, title: str, section_grid: str):
        """Update the gallery grid."""
        grid_title = to_section_title(title)
        gird = grid_title + section_grid
        self.grid_str += gird

    def convert_gallery_header_file(self):
        """Convert the gallery header file."""
        append_string_to_rst_file(
            self.header_file, self.gallery_dir / "index.rst", self.toc
        )
        append_string_to_rst_file(
            self.header_file, self.gallery_dir / "index.rst", self.grid
        )

    def convert(self):
        """Convert the examples to gallery."""
        for folder in self.folders:
            section = SectionGenerator(
                folder / "GALLERY_HEADER.rst",
                self.examples_dir,
                self.gallery_dir,
                self.thumb_strategy,
                self.thumb_strategy_notebook,
                self.default_thumb,
            )
            section.convert()
            self.update_gallery_toc(section.gallery_header_file)

            title = get_rst_title(section.gallery_header_file)
            self.update_gallery_grid(title, section.grid)
        self.convert_gallery_header_file()


class SectionGenerator:
    """
    A class to generate the gallery section for a subfolder.
    """

    def __init__(
        self,
        example_header_file: Path,
        examples_dir: Path,
        gallery_dir: Path,
        thumb_strategy: Literal["first", "last"] = "first",
        thumb_strategy_notebook: Literal["code", "markdown"] = "code",
        default_thumb: Path | str = None,
    ) -> None:
        """Initialize the SectionGenerator object.

        example_header_file : Path
            The path to the example header file.
        examples_dir: Path,
            The path to the input examples directory.
        gallery_dir : Path
            The path to the output gallery directory.
        """
        self.thumb_strategy = thumb_strategy
        self.thumb_strategy_notebook = thumb_strategy_notebook
        self.default_thumb = default_thumb

        self.examples_dir = Path(examples_dir)
        self.gallery_dir = Path(gallery_dir)
        self._example_header_file = Path(example_header_file)

        self._parse_example_files()
        self._parse_gallery_header_file()

        self.grid_item_card_str = ""
        self.toc_str = ""

    def _parse_example_files(self):
        """Parse the example files in the subfolder."""
        files = self._example_header_file.parent.glob("*")
        example_files = []
        for _file in files:
            if _file.suffix in [".ipynb", ".md", ".rst"] and not _file.samefile(
                self._example_header_file
            ):
                example_files.append(_file)
        self._example_files = sorted(example_files)

    def _to_gallery_path(self, example_file: Path) -> Path:
        """Convert the example file path to the gallery path."""
        return self.gallery_dir / example_file.relative_to(self.examples_dir)

    def _parse_gallery_header_file(self):
        """Parse the gallery header file."""
        header_file = self.gallery_dir / self._example_header_file.relative_to(
            self.examples_dir
        )
        gallery_header_file = header_file.parent / f"index{header_file.suffix}"
        folder, name = remove_num_prefix(gallery_header_file)
        self._gallery_header_file = self.gallery_dir / folder / name

    @property
    def example_header_file(self) -> Path:
        """path to the gallery header file."""
        return self._example_header_file

    @property
    def gallery_header_file(self) -> Path:
        """path to the output gallery header file."""
        return self._gallery_header_file

    @property
    def example_files(self) -> list[Path]:
        """path to the example files in a same subfolder."""
        return self._example_files

    @property
    def toc(self) -> str:
        """The table of contents for the gallery subsection."""
        return toc_gallery + self.toc_str

    @property
    def grid(self) -> str:
        """The grid for the gallery subsection."""
        return grid + self.grid_item_card_str

    def update_section_grid_card(self, target_ref: str, img_path: str) -> str:
        """Update the toc and grid item card string ."""
        self.grid_item_card_str += grid_item_card.format(
            target_ref=target_ref, img_path=img_path
        )

    def update_section_toc(self, gallery_file: str):
        """Update the toc string."""
        self.toc_str += f"\n    {gallery_file.stem}"

    def convert_section_header_file(self):
        """Convert the header file of the subfolder to a standardized header file,
        which contains toc and grid cards for the gallery section.
        """
        append_string_to_rst_file(
            self.example_header_file, self.gallery_header_file, self.toc
        )

        append_string_to_rst_file(
            self.example_header_file, self.gallery_header_file, self.grid
        )

    def convert(self):
        """Convert the example files to standardized example files."""
        for example_file in self.example_files:
            conv = ExampleConverter(
                example_file,
                self.examples_dir,
                self.gallery_dir,
                self.thumb_strategy,
                self.thumb_strategy_notebook,
                self.default_thumb,
            )
            conv.convert()
            self.update_section_grid_card(conv.target_ref, conv.gallery_thumb)
            self.update_section_toc(conv.gallery_file)

        self.convert_section_header_file()


class ExampleConverter:
    """
    A class to convert an example (notebook/md/rst) to a standardized example
    file, which is used to generate the gallery.
    """

    _file_type: Literal["notebook", "markdown", "rst"]
    _gallery_thumb: Path

    def __init__(
        self,
        example_file: Path | str,
        examples_dir: Path | str,
        gallery_dir: Path | str,
        thumb_strategy: Literal["first", "last"] = "first",
        thumb_strategy_notebook: Literal["code", "markdown"] = "code",
        default_thumb: Path | str = None,
    ) -> None:
        """Initialize the ExampleConverter.

        example_file : Path | str
            The path to the example file.
        examples_dir : Path | str
            The path to the input examples directory.
        gallery_dir : Path | str
            The path to the output gallery directory.
        thumb_strategy : Literal["first", "last"]
            The strategy for selecting the thumbnail image if multiple images
            are found in the example file.
        default_thumb : Path | str
            The default thumbnail image to use if no image is found in the example
            file.
        """
        self.thumb_strategy = thumb_strategy
        self.thumb_strategy_notebook = thumb_strategy_notebook
        self._example_file = Path(example_file)
        self.examples_dir = Path(examples_dir)
        self.gallery_dir = Path(gallery_dir)
        _ensure_dir_exists(self.gallery_dir)

        (
            self._gallery_file,
            self._thumb_dir,
            self._default_thumb,
            self._relative_path,
        ) = self._parse_paths(default_thumb)
        self._parse_example_type()

    def _parse_paths(self, default_thumb: Path | str = None):
        """Parse the paths for the example file."""
        # thumb
        thumb_dir = self.gallery_dir / "thumbs"
        if default_thumb is None:
            default_thumb = thumb_dir / "no_image.png"
        else:
            default_thumb = Path(default_thumb)

        # relative path
        relative_path = self.example_file.relative_to(self.examples_dir)

        _gallery_file = self.gallery_dir / relative_path
        if not _gallery_file.parent.parent.samefile(self.gallery_dir):
            raise ValueError(
                f"Too many levels of subfolders in the example file: {self.example_file}\n"
                "only one level of subfolders is allowed."
            )

        # Remove the index prefix from the folder and file name for the gallery file
        folder, name = remove_num_prefix(_gallery_file)

        gallery_file = self.gallery_dir / folder / name
        return gallery_file, thumb_dir, default_thumb, relative_path

    def _parse_example_type(self) -> Literal["notebook", "markdown", "rst"]:
        """Parse the example file type."""
        if self.example_file.suffix == ".ipynb":
            file_type = "notebook"
        elif self.example_file.suffix == ".md":
            file_type = "markdown"
        elif self.example_file.suffix == ".rst":
            file_type = "rst"
        else:
            raise ValueError(
                f"Unrecognized file type: {self.example_file.suffix} for {self.example_file}"
            )
        self._file_type = file_type

    @property
    def file_type(self) -> Literal["notebook", "markdown", "rst"]:
        """the file type of the example file."""
        return self._file_type

    @property
    def relative_path(self) -> str:
        """the relative path of the example file."""
        return self._relative_path.as_posix()

    @property
    def example_file(self) -> Path:
        """path to the input example file."""
        return self._example_file

    @property
    def gallery_file(self) -> Path:
        """path to the output gallery file."""
        return self._gallery_file

    @property
    def target_str(self) -> str:
        """the target string in the gallery file used to link to the example file."""
        if self.file_type in ["notebook", "markdown"]:
            return f"({self.target_ref})="
        else:
            return f".. _{self.target_ref}:"

    @property
    def target_ref(self) -> str:
        """the target reference for the example file."""
        return f"example_{self.example_file.stem}"

    @property
    def gallery_thumb(self) -> Path:
        """path to the thumbnail image for the gallery."""
        return self._gallery_thumb

    @property
    def thumb_dir(self) -> Path:
        """path to the thumbs directory."""
        return self._thumb_dir

    @property
    def default_thumb(self) -> Path:
        """path to the default thumbnail image."""
        return self._default_thumb

    @property
    def thumb_idx(self) -> int:
        """The index of the thumbnail image to use."""
        if self.thumb_strategy == "first":
            return 0
        elif self.thumb_strategy == "last":
            return -1
        else:
            raise ValueError(f"Unrecognized thumb_strategy: {self.thumb_strategy}")

    def _load_content(self):
        """Load the content of the example file."""
        with open(self.example_file, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_doc_thumb(self, images: DocImages):
        """Parse the thumb to be used in the gallery.

        Returns
        -------
        exists : bool
            Whether the thumb exists in the example file.
        """
        exists = True
        if len(images) > 0:
            thumbs = images.sel_urls("gallery_thumbnail")
            if len(thumbs) > 0:
                self._gallery_thumb = thumbs[self.thumb_idx]
            else:
                self._gallery_thumb = images[self.thumb_idx]
        else:
            exists = False
            self._gallery_thumb = self.default_thumb

        return exists

    def _parse_cell_thumb(self, images: CellImages):
        """Parse the thumb to be used in the gallery.

        Returns
        -------
        exists : bool
            Whether the thumb exists in the example file.
        """
        exists = True
        if len(images) > 0:
            thumb_file = (
                self.gallery_file.parent / f"{self.example_file.stem}_thumb.png"
            )
            images.save_image(thumb_file, self.thumb_idx)
            self._gallery_thumb = thumb_file
        else:
            exists = False
            self._gallery_thumb = self.default_thumb
        return exists

    def _parse_thumb(self):
        """Parse the thumb to be used in the gallery."""
        content = self._load_content()
        if self.file_type == "markdown":
            images = parse_md_images(content)
            self._parse_doc_thumb(images)
        elif self.file_type == "rst":
            images = parse_rst_images(content)
            self._parse_doc_thumb(images)
        elif self.file_type == "notebook":
            if self.thumb_strategy_notebook == "markdown":
                images = parse_md_images(content)
                if not self._parse_doc_thumb(images):
                    self._parse_cell_thumb(CellImages(self.example_file))
            elif self.thumb_strategy_notebook == "code":
                if not self._parse_cell_thumb(CellImages(self.example_file)):
                    images = parse_md_images(content)
                    self._parse_doc_thumb(images)
            else:
                raise ValueError(
                    f"Unrecognized thumb_strategy_notebook: {self.thumb_strategy_notebook}"
                )

    def _convert_notebook_file(self):
        """Convert a notebook to a standardized example file."""
        with open(self.example_file, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Add a reference to the notebook in the notebook
        new_cell = nbformat.v4.new_markdown_cell(self.target_str)
        notebook.cells.insert(0, new_cell)

        _ensure_dir_exists(self.gallery_file.parent)
        with open(self.gallery_file, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

    def _convert_text_file(self):
        """Convert a text file (md, rst) to a standardized example file."""
        with open(self.example_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add a reference to the markdown/rst file
        new_content = f"{self.target_str}\n\n{content}"
        _ensure_dir_exists(self.gallery_file.parent)
        with open(self.gallery_file, "w", encoding="utf-8") as f:
            f.write(new_content)

    def convert(self):
        """Convert the example file to a standardized example file."""
        if self.file_type == "notebook":
            self._convert_notebook_file()
        elif self.file_type in ["markdown", "rst"]:
            self._convert_text_file()

        self._parse_thumb()
        self._parse_thumb()


def _ensure_dir_exists(directory: Path):
    """Ensure that the directory exists."""
    if not directory.exists():
        directory.mkdir(parents=True)


def append_string_to_rst_file(
    header_in: Path,
    header_out: Path,
    append_str: str,
):
    """Append the gallery string to the gallery header file.

    Parameters
    ----------
    header_in : Path
        The path to the gallery header file.
    header_out : Path
        The path to the output gallery header file.
    append_str : str
        The string to append to the gallery header file.
    """
    if not header_out.exists():
        header_out.parent.mkdir(parents=True, exist_ok=True)
        with open(header_out, "w", encoding="utf-8") as dst:
            with open(header_in, "r", encoding="utf-8") as src:
                content = src.read() + append_str
            dst.write(content)
    else:
        with open(header_out, "a", encoding="utf-8") as f:
            f.write(append_str)


def get_rst_title(file_path: Path) -> str | None:
    """Get the title of a reStructuredText file."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    doctree = publish_doctree(content)

    title_node = doctree.next_node(title)

    if title_node:
        return title_node.astext().strip()
    else:
        return None


def to_section_title(title: str) -> str:
    """Convert a title to a reStructuredText section title."""
    header_line = "-" * len(title)
    sec_title = f"\n\n{title}\n{header_line}\n"
    return sec_title


def remove_num_prefix(gallery_file):
    """Remove the number prefix from the gallery file."""
    folder, name = gallery_file.parent.stem, gallery_file.name
    if folder.split("-")[0].isdigit():
        folder = "-".join(folder.split("-")[1:])
    if name.split("-")[0].isdigit():
        name = "-".join(name.split("-")[1:])
    return folder, name
