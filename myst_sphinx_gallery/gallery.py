"""
A module for managing the gallery of examples.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Literal

import nbformat
from docutils.core import publish_doctree
from docutils.nodes import title

from .config import GalleryConfig
from .grid import Grid, GridItemCard, TocTree
from .images import (
    CellImages,
    DocImages,
    Thumbnail,
    load_nb_markdown,
    parse_md_images,
    parse_rst_images,
)
from .utils import ensure_dir_exists, print_run_time, safe_remove_file


@print_run_time
def generate_gallery(gallery_config: GalleryConfig | dict):
    """Generate the gallery from the examples directory."""
    if isinstance(gallery_config, dict):
        gallery_config = GalleryConfig(**gallery_config)

    n_gallery = len(gallery_config.gallery_dirs)
    for i in range(n_gallery):
        gallery = GalleryGenerator(
            gallery_config.examples_dirs[i],
            gallery_config.gallery_dirs[i],
            gallery_config,
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
        config: GalleryConfig,
    ) -> None:
        """Initialize the GalleryGenerator object.

        examples_dir: Path,
            The path to the input examples directory.
        gallery_dir : Path
            The path to the output gallery directory.
        config : GalleryConfig
            The gallery configuration.
        """
        self.config = config

        self.examples_dir = Path(examples_dir).absolute()
        self.gallery_dir = Path(gallery_dir).absolute()

        self._header_file = self._scan_header_file()
        self._folders = self._scan_example_folders()

        self._toc_tree = config.toc_tree.copy()
        self._grid = config.grid.copy()
        self._grid_item_card = config.grid_item_card.copy()

        self._sections = ""

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
            warnings.warn(
                f"No valid subfolders found in {self.examples_dir}", stacklevel=1
            )
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
    def target_str(self) -> str:
        """the target string in the gallery file used to link to the example file."""
        target_ref = (
            f"{self.config.target_prefix}{self.index_file.parent.stem}_header".lower()
        )
        return f".. _{target_ref}:"

    @property
    def toc(self) -> str:
        """The table of contents string for the gallery."""
        return str(self._toc_tree)

    @property
    def sections(self) -> str:
        """The sections for the gallery."""
        return self._sections

    @property
    def toc_tree(self) -> TocTree:
        """The table of contents tree options for the gallery."""
        return self._toc_tree.copy()

    @property
    def grid(self) -> Grid:
        """The grid options for the gallery."""
        return self._grid.copy()

    @property
    def grid_item_card(self) -> GridItemCard:
        """The grid item card options for the gallery."""
        return self._grid_item_card.copy()

    def add_toc_item(self, section_index_file: str):
        """add a toc item for the gallery."""
        item = self._toc_tree.parse_item(section_index_file, self.gallery_dir)
        self._toc_tree.add_item(item)

    def add_section_item(self, title: str, section_grid: str):
        """add a section item to the gallery."""
        title = to_section_title(title)
        section = title + section_grid
        self._sections += section

    def convert_to_index_file(self):
        """Convert the gallery header file."""
        safe_remove_file(self.index_file)
        write_index_file(self.header_file, self.index_file, self.toc, self.target_str)
        write_index_file(self.header_file, self.index_file, self.sections)

    def convert(self):
        """Convert the examples to gallery."""
        for folder in self.folders:
            section = SectionGenerator(
                folder / "GALLERY_HEADER.rst",
                self.examples_dir,
                self.gallery_dir,
                self.config,
            )
            section.convert()
            self.add_toc_item(section.index_file)
            title = get_rst_title(section.header_file)
            self.add_section_item(title, section.section_grid)
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
        config: GalleryConfig,
    ) -> None:
        """Initialize the SectionGenerator object.

        header_file : Path
            The path to the example header file.
        examples_dir: Path,
            The path to the input examples directory.
        gallery_dir : Path
            The path to the output gallery directory.
        config : GalleryConfig
            The gallery configuration.
        """
        self.examples_dir = Path(examples_dir)
        self.gallery_dir = Path(gallery_dir)
        self._header_file = Path(header_file)
        self._config = config

        self._example_files = self._scan_example_files()
        self._index_file = self._parse_index_file()

        self._toc_tree = config.toc_tree.copy()
        self._grid = config.grid.copy()
        self._grid_item_card = config.grid_item_card.copy()

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
    def config(self) -> GalleryConfig:
        """The gallery configuration."""
        return self._config

    @property
    def header_file(self) -> Path:
        """path to the gallery header file."""
        return self._header_file

    @property
    def index_file(self) -> Path:
        """path to the output gallery header file."""
        return self._index_file

    @property
    def target_str(self) -> str:
        """the target string in the gallery file used to link to the example file."""
        target_ref = (
            f"{self.config.target_prefix}{self.index_file.parent.stem}_header".lower()
        )
        return f".. _{target_ref}:"

    @property
    def example_files(self) -> list[Path]:
        """path to the example files in a same subfolder."""
        return self._example_files

    @property
    def toc(self) -> str:
        """The table of contents for gallery section."""
        return str(self._toc_tree)

    @property
    def section_grid(self) -> str:
        """The grid for the gallery section."""
        return str(self._grid)

    @property
    def toc_tree(self) -> TocTree:
        """The table of contents options for gallery section."""
        return self._toc_tree.copy()

    @property
    def grid(self) -> Grid:
        """The grid options for gallery section."""
        return self._grid.copy()

    @property
    def grid_item_card(self) -> GridItemCard:
        """The grid item card options for gallery section."""
        return self._grid_item_card.copy()

    def add_grid_card(self, target_ref: str, img_path: str) -> str:
        """add a grid card for the gallery section grid."""
        self._grid.add_item(self._grid_item_card.format(target_ref, img_path))

    def add_example_to_toc(self, gallery: str):
        """add a example to the table of contents of section."""
        self._toc_tree.add_item(gallery.stem)

    def convert_section_header_file(self):
        """Convert the header file of the subfolder to a standardized header file,
        which contains toc and grid cards for the gallery section.
        """
        safe_remove_file(self.index_file)
        write_index_file(self.header_file, self.index_file, self.toc, self.target_str)
        write_index_file(self.header_file, self.index_file, self.section_grid)

    def convert(self):
        """Convert the example files to standardized example files."""
        for example_file in self.example_files:
            conv = ExampleConverter(
                example_file, self.examples_dir, self.gallery_dir, self.config
            )
            conv.convert()
            self.add_grid_card(conv.target_ref, conv.gallery_thumb)
            self.add_example_to_toc(conv.gallery_file)

        self.convert_section_header_file()


class ExampleConverter:
    """
    A class to convert an example (notebook/md/rst) to a standardized example
    file, which is used to generate the gallery.
    """

    _file_type: Literal["notebook", "markdown", "rst"]
    _gallery_thumb: Path | None = None
    _thumbnail: Thumbnail | None = None

    def __init__(
        self,
        example_file: Path | str,
        examples_dir: Path | str,
        gallery_dir: Path | str,
        config: GalleryConfig,
    ) -> None:
        """Initialize the ExampleConverter.

        example_file : Path | str
            The path to the example file.
        examples_dir : Path | str
            The path to the input examples directory.
        gallery_dir : Path | str
            The path to the output gallery directory.
        config : GalleryConfig
            The gallery configuration.
        """
        self._config = config
        self.thumbnail_strategy = config.thumbnail_strategy
        self.notebook_thumbnail_strategy = config.notebook_thumbnail_strategy
        self._example_file = Path(example_file)
        self.examples_dir = Path(examples_dir)
        self.gallery_dir = Path(gallery_dir)
        ensure_dir_exists(self.gallery_dir)

        self._gallery_file, self._relative_path = self._parse_paths()
        self._file_type = self._parse_example_type()
        self._default_thumb = self._ensure_default_thumb(config.default_thumbnail_file)
        self._thumbnail = None

    def _ensure_default_thumb(self, default_thumb: Path | str) -> Path:
        """Ensure the default thumbnail image exists."""
        if default_thumb is None:
            default_thumb = default_thumbnail()
        return Path(default_thumb)

    def _parse_paths(self):
        """Parse the paths for the example file."""
        # relative path
        relative_path = self.example_file.relative_to(self.examples_dir)

        gallery_file = self.gallery_dir / relative_path
        if not gallery_file.parent.parent.samefile(self.gallery_dir):
            raise ValueError(
                f"Too many levels of subfolders in the example file: {self.example_file}\n"
                "only one level of subfolders is allowed."
            )

        # Remove the index prefix from the folder and file name for the gallery file
        folder, name = remove_num_prefix(gallery_file)

        gallery_file = self.gallery_dir / folder / name
        return gallery_file, relative_path

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
    def config(self) -> GalleryConfig:
        """The gallery configuration."""
        return self._config

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
        return f"{self.config.target_prefix}{self.gallery_file.stem}".lower()

    @property
    def gallery_thumb(self) -> Path:
        """path to the thumbnail image for the gallery."""
        return self._gallery_thumb

    @property
    def default_thumb(self) -> Path:
        """path to the default thumbnail image."""
        return self._default_thumb

    @property
    def thumb_dir(self) -> Path:
        """path to the thumbnail directory for the example."""
        return self.gallery_dir / "myst_sphinx_gallery_thumbs"

    @property
    def no_image_thumb(self) -> Path:
        """path to the no image thumbnail."""
        return self.thumb_dir / "no_image.webp"

    def thumb_file_rel(self, thumb_file: Path) -> str:
        """relative path to the thumbnail image for the example."""
        thumb_file_rel = thumb_file.relative_to(self.gallery_dir).as_posix()
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
        with open(self.example_file, encoding="utf-8") as f:
            return f.read()

    def _use_default_thumbnail(self):
        """Use the default thumbnail image as the gallery file thumb."""
        self._gallery_thumb = self.thumb_file_rel(self.no_image_thumb)
        if self.no_image_thumb.exists():
            return

        thumbnail = Thumbnail(
            self.default_thumb, self.thumb_dir, **self.config.thumbnail_config.to_dict()
        )
        thumbnail.save_thumbnail(self.no_image_thumb)

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
                gallery_thumb = thumbs[self.thumb_idx]
            else:
                gallery_thumb = images[self.thumb_idx]
            gallery_thumb = self.config.abs_path(gallery_thumb)
            thumbnail = Thumbnail(
                gallery_thumb, self.thumb_dir, **self.config.thumbnail_config.to_dict()
            )
            gallery_thumb = thumbnail.save_thumbnail()
            self._gallery_thumb = self.thumb_file_rel(gallery_thumb)
        else:
            exists = False
            self._use_default_thumbnail()

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
            gallery_thumb = self.thumb_dir / f"{self.example_file.stem}.webp"
            thumbnail = Thumbnail(
                images.images[self.thumb_idx],
                self.thumb_dir,
                **self.config.thumbnail_config.to_dict(),
            )
            thumbnail.save_thumbnail(gallery_thumb)
            self._gallery_thumb = self.thumb_file_rel(gallery_thumb)
        else:
            exists = False
            self._use_default_thumbnail()

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
        with open(self.example_file, encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Add a reference to the notebook in the notebook
        new_cell = nbformat.v4.new_markdown_cell(self.target_str)
        notebook.cells.insert(0, new_cell)

        ensure_dir_exists(self.gallery_file.parent)
        with open(self.gallery_file, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

    def _convert_text_file(self):
        """Convert a text file (md, rst) to a standardized example file."""
        with open(self.example_file, encoding="utf-8") as f:
            content = f.read()

        # Add a reference to the markdown/rst file
        new_content = f"{self.target_str}\n\n{content}"
        ensure_dir_exists(self.gallery_file.parent)
        with open(self.gallery_file, "w", encoding="utf-8") as f:
            f.write(new_content)

    def convert(self):
        """Convert the example file to a standardized example file."""
        if self.file_type == "notebook":
            self._convert_notebook_file()
        elif self.file_type in ["markdown", "rst"]:
            self._convert_text_file()

        self._parse_thumb()


def write_index_file(
    header_file: Path,
    index_file: Path,
    append_str: str,
    prepend_str: str = "",
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
            with open(header_file, encoding="utf-8") as src:
                content = f"{prepend_str}\n\n{src.read()}\n{append_str}"
            dst.write(content)
    else:
        # only append the string if the file exists
        with open(index_file, "a", encoding="utf-8") as dst:
            dst.write(append_str)


def get_rst_title(file_path: Path) -> str | None:
    """Get the title of a reStructuredText file."""
    with open(file_path, encoding="utf-8") as file:
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
