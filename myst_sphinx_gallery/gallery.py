"""
A module for managing the gallery of examples.
"""

import shutil
import warnings
from pathlib import Path
from typing import Literal

import nbformat
from docutils.core import publish_doctree
from docutils.nodes import title

from .config import GalleryConfig
from .images import (
    CellImages,
    DocImages,
    load_nb_markdown,
    parse_md_images,
    parse_rst_images,
)
from .patterns import grid, grid_item_card, toc_gallery


def generate_gallery(gallery_config: GalleryConfig):
    """Generate the gallery from the examples directory."""
    n_gallery = len(gallery_config.gallery_dirs)
    for i in range(n_gallery):
        gallery = GalleryGenerator(
            gallery_config.examples_dirs[i],
            gallery_config.gallery_dirs[i],
            gallery_config.thumbnail_strategy,
            gallery_config.notebook_thumbnail_strategy,
            gallery_config.default_thumbnail_file,
        )
        gallery.convert()


class GalleryGenerator:
    """
    A class to generate the gallery for a folder.
    """

    def __init__(
        self,
        examples_dir: Path,
        gallery_dir: Path,
        thumbnail_strategy: Literal["first", "last"] = "first",
        notebook_thumbnail_strategy: Literal["code", "markdown"] = "code",
        default_thumb: Path | str = None,
    ) -> None:
        """Initialize the GalleryGenerator object.

        examples_dir: Path,
            The path to the input examples directory.
        gallery_dir : Path
            The path to the output gallery directory.
        thumbnail_strategy : Literal["first", "last"]
            The strategy for selecting the thumbnail image if multiple images
            are found in the example file.
        notebook_thumbnail_strategy : Literal["code", "markdown"]
            The strategy for selecting the thumbnail image if multiple images
            are found in the example file.
        default_thumb : Path | str
            The default thumbnail image to use if no image is found in the example
            file.
        """
        self.thumbnail_strategy = thumbnail_strategy
        self.notebook_thumbnail_strategy = notebook_thumbnail_strategy
        self.default_thumb = default_thumb

        self.examples_dir = Path(examples_dir).absolute()
        self.gallery_dir = Path(gallery_dir).absolute()

        self._header_file = self._scan_header_file()
        self._folders = self._scan_example_folders()

        self.toc_str = ""
        self.grid_str = ""

    def _scan_header_file(self):
        """Scan header file for the whole gallery."""
        header_file = self.examples_dir / "GALLERY_HEADER.rst"
        if not header_file.exists():
            raise FileNotFoundError(f"Gallery header file not found: {header_file}")
        return header_file

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
        return sorted(folders)

    @property
    def folders(self) -> list[Path]:
        """Folders that contain example files."""
        return self._folders

    @property
    def header_file(self) -> Path:
        """The path to the input example header file."""
        return self._header_file

    @property
    def index_file(self) -> Path:
        """The path to the output gallery index file."""
        return self.gallery_dir / "index.rst"

    @property
    def toc(self) -> str:
        """The table of contents for the gallery."""
        return toc_gallery + self.toc_str

    @property
    def grid(self) -> str:
        """The grid for the gallery."""
        return self.grid_str

    def add_toc_item(self, section_index_file: str):
        """Update the gallery table of contents."""
        rel_path = section_index_file.relative_to(self.gallery_dir)
        self.toc_str += f"\n    {rel_path}"

    def add_grid_item(self, title: str, section_grid: str):
        """Update the gallery grid."""
        grid_title = to_section_title(title)
        gird = grid_title + section_grid
        self.grid_str += gird

    def convert_to_index_file(self):
        """Convert the gallery header file."""
        safe_remove_file(self.index_file)
        write_index_file(self.header_file, self.index_file, self.toc)
        write_index_file(self.header_file, self.index_file, self.grid)

    def convert(self):
        """Convert the examples to gallery."""
        for folder in self.folders:
            section = SectionGenerator(
                folder / "GALLERY_HEADER.rst",
                self.examples_dir,
                self.gallery_dir,
                self.thumbnail_strategy,
                self.notebook_thumbnail_strategy,
                self.default_thumb,
            )
            section.convert()
            self.add_toc_item(section.index_file)
            title = get_rst_title(section.index_file)
            self.add_grid_item(title, section.grid)
        self.convert_to_index_file()


class SectionGenerator:
    """
    A class to generate the gallery section for a subfolder.
    """

    def __init__(
        self,
        header_file: Path,
        examples_dir: Path,
        gallery_dir: Path,
        thumbnail_strategy: Literal["first", "last"] = "first",
        notebook_thumbnail_strategy: Literal["code", "markdown"] = "code",
        default_thumb: Path | str = None,
    ) -> None:
        """Initialize the SectionGenerator object.

        header_file : Path
            The path to the example header file.
        examples_dir: Path,
            The path to the input examples directory.
        gallery_dir : Path
            The path to the output gallery directory.
        """
        self.thumbnail_strategy = thumbnail_strategy
        self.notebook_thumbnail_strategy = notebook_thumbnail_strategy
        self.default_thumb = default_thumb

        self.examples_dir = Path(examples_dir)
        self.gallery_dir = Path(gallery_dir)
        self._header_file = Path(header_file)

        self._example_files = self._scan_example_files()
        self._index_file = self._parse_index_file()

        self.grid_item_card_str = ""
        self.toc_str = ""

    def _scan_example_files(self):
        """Parse the example files in the subfolder."""
        files = self._header_file.parent.glob("*")
        example_files = []
        for _file in files:
            if _file.suffix in [".ipynb", ".md", ".rst"] and not _file.samefile(
                self._header_file
            ):
                example_files.append(_file)
        return sorted(example_files)

    def _to_gallery_path(self, example_file: Path) -> Path:
        """Convert the example file path to the gallery path."""
        return self.gallery_dir / example_file.relative_to(self.examples_dir)

    def _parse_index_file(self):
        """Parse the gallery index file."""
        index_file = self.gallery_dir / self.header_file.relative_to(self.examples_dir)
        index_file = index_file.with_name("index.rst")
        folder, name = remove_num_prefix(index_file)
        index_file = self.gallery_dir / folder / name
        return index_file

    @property
    def header_file(self) -> Path:
        """path to the gallery header file."""
        return self._header_file

    @property
    def index_file(self) -> Path:
        """path to the output gallery header file."""
        return self._index_file

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

    def update_section_toc(self, index_file: str):
        """Update the toc string."""
        self.toc_str += f"\n    {index_file.stem}"

    def convert_section_header_file(self):
        """Convert the header file of the subfolder to a standardized header file,
        which contains toc and grid cards for the gallery section.
        """
        safe_remove_file(self.index_file)
        write_index_file(self.header_file, self.index_file, self.toc)
        write_index_file(self.header_file, self.index_file, self.grid)

    def convert(self):
        """Convert the example files to standardized example files."""
        for example_file in self.example_files:
            conv = ExampleConverter(
                example_file,
                self.examples_dir,
                self.gallery_dir,
                self.thumbnail_strategy,
                self.notebook_thumbnail_strategy,
                self.default_thumb,
            )
            conv.convert()
            self.update_section_grid_card(conv.target_ref, conv.gallery_thumb)
            self.update_section_toc(conv.index_file)

        self.convert_section_header_file()


class ExampleConverter:
    """
    A class to convert an example (notebook/md/rst) to a standardized example
    file, which is used to generate the gallery.
    """

    _file_type: Literal["notebook", "markdown", "rst"]
    _gallery_thumb: Path | None = None
    _thumbnail: Path | None = None

    def __init__(
        self,
        example_file: Path | str,
        examples_dir: Path | str,
        gallery_dir: Path | str,
        thumbnail_strategy: Literal["first", "last"] = "first",
        notebook_thumbnail_strategy: Literal["code", "markdown"] = "code",
        default_thumb: Path | str = None,
    ) -> None:
        """Initialize the ExampleConverter.

        example_file : Path | str
            The path to the example file.
        examples_dir : Path | str
            The path to the input examples directory.
        gallery_dir : Path | str
            The path to the output gallery directory.
        thumbnail_strategy : Literal["first", "last"]
            The strategy for selecting the thumbnail image if multiple images
            are found in the example file.
        default_thumb : Path | str
            The default thumbnail image to use if no image is found in the example
            file.
        """
        self.thumbnail_strategy = thumbnail_strategy
        self.notebook_thumbnail_strategy = notebook_thumbnail_strategy
        self._example_file = Path(example_file)
        self.examples_dir = Path(examples_dir)
        self.gallery_dir = Path(gallery_dir)
        ensure_dir_exists(self.gallery_dir)

        self._index_file, self._relative_path = self._parse_paths()
        self._file_type = self._parse_example_type()
        self._default_thumb = self._ensure_default_thumb(default_thumb)

    def _ensure_default_thumb(self, default_thumb: Path | str) -> Path:
        """Ensure the default thumbnail image exists."""
        if default_thumb is None:
            default_thumb = default_thumbnail()
        return Path(default_thumb)

    def _parse_paths(self):
        """Parse the paths for the example file."""
        # relative path
        relative_path = self.example_file.relative_to(self.examples_dir)

        _index_file = self.gallery_dir / relative_path
        if not _index_file.parent.parent.samefile(self.gallery_dir):
            raise ValueError(
                f"Too many levels of subfolders in the example file: {self.example_file}\n"
                "only one level of subfolders is allowed."
            )

        # Remove the index prefix from the folder and file name for the gallery file
        folder, name = remove_num_prefix(_index_file)

        index_file = self.gallery_dir / folder / name
        return index_file, relative_path

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
        return file_type

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
    def index_file(self) -> Path:
        """path to the output gallery file."""
        return self._index_file

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
    def default_thumb(self) -> Path:
        """path to the default thumbnail image."""
        return self._default_thumb

    @property
    def thumb_file(self) -> Path:
        """path to the thumbnail image for the example."""
        folder = self.gallery_dir / "myst_sphinx_gallery_thumbs"
        ensure_dir_exists(folder)
        thumb_file = folder / f"{self.index_file.stem}_thumb.png"
        return thumb_file

    @property
    def thumb_file_rel(self) -> str:
        """relative path to the thumbnail image for the example."""
        thumb_file_rel = self.thumb_file.relative_to(self.gallery_dir).as_posix()
        thumb_file_rel = f"/{self.gallery_dir.stem}/{thumb_file_rel}"
        return thumb_file_rel

    @property
    def thumb_idx(self) -> int:
        """The index of the thumbnail image to use."""
        if self.thumbnail_strategy == "first":
            return 0
        elif self.thumbnail_strategy == "last":
            return -1
        else:
            raise ValueError(
                f"Unrecognized thumbnail_strategy: {self.thumbnail_strategy}"
            )

    def _load_content(self):
        """Load the content of the example file."""
        if self.file_type == "notebook":
            return load_nb_markdown(self.example_file)
        with open(self.example_file, "r", encoding="utf-8") as f:
            return f.read()

    def _safe_copy_thumb(self):
        """Copy the thumbnail image to the gallery."""
        if not self.thumb_file.exists():
            shutil.copy(self.default_thumb, self.thumb_file)

    def _parse_doc_thumb(self, images: DocImages):
        """Parse the thumb to be used in the gallery for images cross-referenced in the document.

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
            self._safe_copy_thumb()
            self._gallery_thumb = self.thumb_file_rel

        return exists

    def _parse_cell_thumb(self, images: CellImages):
        """Parse the thumb to be used in the gallery for images in the notebook code cells output.

        Returns
        -------
        exists : bool
            Whether the thumb exists in the example file.
        """
        exists = True
        if len(images) > 0:
            images.save_image(self.thumb_file, self.thumb_idx)
            self._gallery_thumb = self.thumb_file_rel
        else:
            exists = False
            self._safe_copy_thumb()
            self._gallery_thumb = self.thumb_file_rel
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
            if self.notebook_thumbnail_strategy == "markdown":
                images = parse_md_images(content)
                if not self._parse_doc_thumb(images):
                    self._parse_cell_thumb(CellImages(self.example_file))
            elif self.notebook_thumbnail_strategy == "code":
                if not self._parse_cell_thumb(CellImages(self.example_file)):
                    images = parse_md_images(content)
                    self._parse_doc_thumb(images)
            else:
                raise ValueError(
                    f"Unrecognized notebook_thumbnail_strategy: {self.notebook_thumbnail_strategy}"
                )

    def _convert_notebook_file(self):
        """Convert a notebook to a standardized example file."""
        with open(self.example_file, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Add a reference to the notebook in the notebook
        new_cell = nbformat.v4.new_markdown_cell(self.target_str)
        notebook.cells.insert(0, new_cell)

        ensure_dir_exists(self.index_file.parent)
        with open(self.index_file, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

    def _convert_text_file(self):
        """Convert a text file (md, rst) to a standardized example file."""
        with open(self.example_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add a reference to the markdown/rst file
        new_content = f"{self.target_str}\n\n{content}"
        ensure_dir_exists(self.index_file.parent)
        with open(self.index_file, "w", encoding="utf-8") as f:
            f.write(new_content)

    def convert(self):
        """Convert the example file to a standardized example file."""
        if self.file_type == "notebook":
            self._convert_notebook_file()
        elif self.file_type in ["markdown", "rst"]:
            self._convert_text_file()

        self._parse_thumb()


def ensure_dir_exists(directory: Path):
    """Ensure that the directory exists."""
    if not directory.exists():
        directory.mkdir(parents=True)


def safe_remove_file(file: Path):
    """Remove a file if it exists."""
    if file.exists():
        file.unlink()


def write_index_file(
    header_file: Path,
    index_file: Path,
    append_str: str,
):
    """Write/Append string into a gallery header file

    Parameters
    ----------
    header_file : Path
        The path to the example header file.
    index_file : Path
        The path to the output gallery index file.
    append_str : str
        The string to append to the gallery header file.
    """
    ensure_dir_exists(index_file.parent)
    if not index_file.exists():
        # copy and append the header file if not exists
        with open(index_file, "w", encoding="utf-8") as dst:
            with open(header_file, "r", encoding="utf-8") as src:
                content = src.read() + append_str
            dst.write(content)
    else:
        # only append the string if the file exists
        with open(index_file, "a", encoding="utf-8") as dst:
            dst.write(append_str)


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


def remove_num_prefix(header_file: Path) -> tuple[str, str]:
    """Remove the number prefix from the example file/dir."""
    folder, name = header_file.parent.stem, header_file.name
    if folder.split("-")[0].isdigit():
        folder = "-".join(folder.split("-")[1:])
    if name.split("-")[0].isdigit():
        name = "-".join(name.split("-")[1:])
    return folder, name


def default_thumbnail():
    """Return the path to the default thumbnail image."""
    return Path(__file__).parent / "_static" / "no_image.png"
