"""A module for managing the gallery of examples."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import nbformat

from .config import GalleryConfig
from .images import CellImages, DocImages, Thumbnail, parse_md_images, parse_rst_images
from .utils import (
    default_thumbnail,
    ensure_dir_exists,
    get_rst_title,
    load_nb_markdown,
    print_run_time,
    remove_num_prefix,
    safe_remove_file,
    to_section_title,
)

if TYPE_CHECKING:
    from .grid import Grid, GridItemCard, TocTree


@print_run_time
def generate_gallery(gallery_config: GalleryConfig | dict) -> None:
    """Generate the gallery from the examples directory.

    Parameters
    ----------
    gallery_config : GalleryConfig | dict
        The gallery configuration.

    """
    if isinstance(gallery_config, dict):
        gallery_config = GalleryConfig(**gallery_config)

    n_gallery = len(gallery_config.gallery_dirs)
    if gallery_config.base_gallery:
        for i in range(n_gallery):
            header_file = gallery_config.examples_dirs[i] / "GALLERY_HEADER.rst"
            gallery = SectionGenerator(
                header_file,
                gallery_config.examples_dirs[i],
                gallery_config.gallery_dirs[i],
                gallery_config,
            )
            gallery.convert()
    else:
        for i in range(n_gallery):
            gallery = GalleryGenerator(
                gallery_config.examples_dirs[i],
                gallery_config.gallery_dirs[i],
                gallery_config,
            )
            gallery.convert()


class GalleryGenerator:
    """A class to generate the gallery for a folder."""

    def __init__(
        self,
        examples_dir: Path,
        gallery_dir: Path,
        config: GalleryConfig,
    ) -> None:
        """Initialize the GalleryGenerator object.

        Parameters
        ----------
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

    def _scan_header_file(self) -> Path:
        """Scan header file for the whole gallery."""
        header_file = self.examples_dir / "GALLERY_HEADER.rst"
        if not header_file.exists():
            msg = f"Gallery header file not found: {header_file}"
            raise FileNotFoundError(msg)
        return header_file

    def _scan_example_folders(self) -> list[Path]:
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
        """The target string in the gallery file used to link to the example file."""
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

    def add_toc_item(self, section_index_file: str) -> None:
        """Add a toc item for the gallery."""
        item = self._toc_tree.parse_item(section_index_file, self.gallery_dir)
        self._toc_tree.add_item(item)

    def add_section_item(self, title: str, section_grid: str) -> None:
        """Add a section item to the gallery."""
        title = to_section_title(title)
        section = title + section_grid
        self._sections += section

    def convert_to_index_file(self) -> None:
        """Convert the gallery header file."""
        safe_remove_file(self.index_file)
        write_index_file(self.header_file, self.index_file, self.toc, self.target_str)
        write_index_file(self.header_file, self.index_file, self.sections)

    def convert(self) -> None:
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
    """A class to generate the gallery section for a subfolder."""

    def __init__(
        self,
        header_file: Path,
        examples_dir: Path,
        gallery_dir: Path,
        config: GalleryConfig,
    ) -> None:
        """Initialize the SectionGenerator object.

        Parameters
        ----------
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
        self.base_gallery = config.base_gallery

        self._example_files = self._scan_example_files()
        self._index_file = self._parse_index_file()

        self._toc_tree = config.toc_tree.copy()
        self._grid = config.grid.copy()
        self._grid_item_card = config.grid_item_card.copy()

    def _scan_example_files(self) -> list[Path]:
        """Parse the example files in the subfolder."""
        files = self._header_file.parent.glob("*")
        example_files = []

        example_files = [
            f
            for f in files
            if f.suffix in [".ipynb", ".md", ".rst"]
            and not f.samefile(self._header_file)
        ]
        return sorted(example_files)

    def _to_gallery_path(self, example_file: Path) -> Path:
        """Convert the example file path to the gallery path."""
        return self.gallery_dir / example_file.relative_to(self.examples_dir)

    def _parse_index_file(self) -> Path:
        """Parse the gallery index file."""
        index_file = self.gallery_dir / self.header_file.relative_to(self.examples_dir)
        index_file = index_file.with_name("index.rst")
        folder, name = remove_num_prefix(index_file)
        if self.base_gallery:
            index_file = self.gallery_dir / name
        else:
            index_file = self.gallery_dir / folder / name
        return index_file

    @property
    def config(self) -> GalleryConfig:
        """The gallery configuration."""
        return self._config

    @property
    def header_file(self) -> Path:
        """Path to the gallery header file."""
        return self._header_file

    @property
    def index_file(self) -> Path:
        """Path to the output gallery header file."""
        return self._index_file

    @property
    def target_str(self) -> str:
        """The target string in the gallery file used to link to the example file."""
        target_ref = (
            f"{self.config.target_prefix}{self.index_file.parent.stem}_header".lower()
        )
        return f".. _{target_ref}:"

    @property
    def example_files(self) -> list[Path]:
        """Path to the example files in a same subfolder."""
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

    def add_grid_card(self, grid_item_card: str) -> str:
        """Add a grid card for the gallery section grid."""
        self._grid.add_item(grid_item_card)

    def add_example_to_toc(self, gallery: str) -> None:
        """Add a example to the table of contents of section."""
        self._toc_tree.add_item(gallery.stem)

    def convert_section_header_file(self) -> None:
        """Convert the header file of the subfolder to a standardized header file.

        New header file will contain toc and grid cards for the gallery section.
        """
        safe_remove_file(self.index_file)
        write_index_file(self.header_file, self.index_file, self.toc, self.target_str)
        write_index_file(self.header_file, self.index_file, self.section_grid)

    def convert(self) -> None:
        """Convert the example files to standardized example files."""
        for example_file in self.example_files:
            conv = ExampleConverter(
                example_file,
                self.examples_dir,
                self.gallery_dir,
                self.config,
            )
            conv.convert()
            self.add_grid_card(conv.grid_item_card)
            self.add_example_to_toc(conv.gallery_file)

        self.convert_section_header_file()


class ExampleConverter:
    """A class to convert an example to a standardized example file.

    notebook, md, rst are all supported.
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
        thumbnail_location: Literal["gallery", "parent"] = "gallery",
        save_thumbnail: bool = True,
    ) -> None:
        """Initialize the ExampleConverter.

        Parameters
        ----------
        example_file : Path | str
            The path to the example file.
        examples_dir : Path | str
            The path to the input examples directory.
        gallery_dir : Path | str
            The path to the output gallery directory.
        config : GalleryConfig
            The gallery configuration.
        thumbnail_location : Literal["gallery", "parent"]
            The location to save the thumbnail image.
        save_thumbnail : bool
            Whether to save the thumbnail image during the conversion.

        """
        self._config = config
        self.base_gallery = config.base_gallery
        self.thumbnail_strategy = config.thumbnail_strategy
        self.notebook_thumbnail_strategy = config.notebook_thumbnail_strategy
        self.thumbnail_location = thumbnail_location
        self.save_thumbnail = save_thumbnail
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

    def _parse_paths(self) -> tuple[Path | None, str | None]:
        """Parse the paths for the example file.

        Returns
        -------
        gallery_file : Path | None
            The path to the output gallery file. If example_dir is None, return None.
        relative_path : str | None
            The relative path of the example file. If example_dir is None, return None.

        """
        # relative path
        if self.examples_dir is None:
            return None, None

        relative_path = self.example_file.relative_to(self.examples_dir)
        gallery_file = self.gallery_dir / relative_path
        if not self.base_gallery and not gallery_file.parent.parent.samefile(
            self.gallery_dir
        ):
            msg = (
                "Too many levels of subfolders in the example file: "
                f"{self.example_file}\nonly one level of subfolders is allowed."
            )
            raise ValueError(msg)

        # Remove the index prefix from the folder and file name for the gallery file
        folder, name = remove_num_prefix(gallery_file)
        if self.base_gallery:
            gallery_file = self.gallery_dir / name
        else:
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
            msg = (
                f"Unrecognized file type: {self.example_file.suffix} for "
                f"{self.example_file}"
            )
            raise ValueError(msg)
        return file_type

    @property
    def config(self) -> GalleryConfig:
        """The gallery configuration."""
        return self._config

    @property
    def file_type(self) -> Literal["notebook", "markdown", "rst"]:
        """The file type of the example file."""
        return self._file_type

    @property
    def relative_path(self) -> str:
        """The relative path of the example file."""
        return self._relative_path.as_posix()

    @property
    def example_file(self) -> Path:
        """Path to the input example file."""
        return self._example_file

    @property
    def gallery_file(self) -> Path:
        """Path to the output gallery file."""
        return self._gallery_file

    @property
    def grid_item_card(self) -> str:
        """The grid item card for the gallery."""
        self._parse_thumb()
        return self.config.grid_item_card.format(self.target_ref, self.gallery_thumb)

    @property
    def target_str(self) -> str:
        """The target string in the gallery file used to link to the example file."""
        if self.file_type in ["notebook", "markdown"]:
            return f"({self.target_ref})="
        return f".. _{self.target_ref}:"

    @property
    def target_ref(self) -> str:
        """The target reference for the example file."""
        return f"{self.config.target_prefix}{self.gallery_file.stem}".lower()

    @property
    def gallery_thumb(self) -> Path:
        """Path to the thumbnail image for the gallery."""
        return self._gallery_thumb

    @property
    def default_thumb(self) -> Path:
        """Path to the default thumbnail image."""
        return self._default_thumb

    @property
    def thumb_dir(self) -> Path:
        """Path to the thumbnail directory for the example."""
        return self.gallery_dir / "myst_sphinx_gallery_thumbs"

    @property
    def no_image_thumb(self) -> Path:
        """Path to the no image thumbnail."""
        return self.thumb_dir / "no_image.webp"

    def thumb_file_rel(self, thumb_file: Path) -> str:
        """Relative path to the thumbnail image for the example."""
        thumb_file_rel = thumb_file.relative_to(self.gallery_dir).as_posix()
        if self.thumbnail_location == "gallery":
            thumb_file_rel = f"{self.gallery_dir.stem}/{thumb_file_rel}"
        return f"/{thumb_file_rel}"

    @property
    def thumb_idx(self) -> int:
        """The index of the thumbnail image to use."""
        if self.thumbnail_strategy == "first":
            return 0
        if self.thumbnail_strategy == "last":
            return -1
        msg = f"Unrecognized thumbnail_strategy: {self.thumbnail_strategy}"
        raise ValueError(msg)

    def _load_content(self) -> str:
        """Load the content of the example file."""
        if self.file_type == "notebook":
            return load_nb_markdown(self.example_file)
        with self.example_file.open(encoding="utf-8") as f:
            return f.read()

    def _use_default_thumbnail(self) -> None:
        """Use the default thumbnail image as the gallery file thumb."""
        self._gallery_thumb = self.thumb_file_rel(self.no_image_thumb)
        if self.no_image_thumb.exists():
            return

        if self.save_thumbnail:
            thumbnail = Thumbnail(
                self.default_thumb,
                self.thumb_dir,
                **self.config.thumbnail_config.to_dict(),
            )
            thumbnail.save_thumbnail(self.no_image_thumb)

    def _parse_doc_thumb(self, images: DocImages) -> bool:
        """Parse thumb to be used in gallery for images cross-referenced.

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
            if self.save_thumbnail:
                gallery_thumb = thumbnail.save_thumbnail()
            else:
                gallery_thumb = thumbnail.auto_output_path
            self._gallery_thumb = self.thumb_file_rel(gallery_thumb)
        else:
            exists = False
            self._use_default_thumbnail()

        return exists

    def _parse_cell_thumb(self, images: CellImages) -> bool:
        """Parse thumb to be used in gallery for images in notebook code cells.

        Returns
        -------
        exists : bool
            Whether the thumb exists in the example file.

        """
        exists = True
        if len(images) > 0:
            gallery_thumb = self.thumb_dir / f"{self.example_file.stem}.webp"
            self._gallery_thumb = self.thumb_file_rel(gallery_thumb)
            if self.save_thumbnail:
                thumbnail = Thumbnail(
                    images[self.thumb_idx],
                    self.thumb_dir,
                    **self.config.thumbnail_config.to_dict(),
                )
                thumbnail.save_thumbnail(gallery_thumb)
        else:
            exists = False
            self._use_default_thumbnail()

        return exists

    def _parse_thumb(self) -> None:
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
                msg = (
                    "Unrecognized notebook_thumbnail_strategy: "
                    f"{self.notebook_thumbnail_strategy}"
                )
                raise ValueError(msg)

    def _convert_notebook_file(self) -> None:
        """Convert a notebook to a standardized example file."""
        with self.example_file.open(encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # Add a reference to the notebook in the notebook
        new_cell = nbformat.v4.new_markdown_cell(self.target_str)
        notebook.cells.insert(0, new_cell)

        ensure_dir_exists(self.gallery_file.parent)
        with self.gallery_file.open("w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

    def _convert_text_file(self) -> None:
        """Convert a text file (md, rst) to a standardized example file."""
        with self.example_file.open(encoding="utf-8") as f:
            content = f.read()

        # Add a reference to the markdown/rst file
        new_content = f"{self.target_str}\n\n{content}"
        ensure_dir_exists(self.gallery_file.parent)
        with self.gallery_file.open("w", encoding="utf-8") as f:
            f.write(new_content)

    def convert(self) -> None:
        """Convert the example file to a standardized example file."""
        if self.file_type == "notebook":
            self._convert_notebook_file()
        elif self.file_type in ["markdown", "rst"]:
            self._convert_text_file()


def write_index_file(
    header_file: Path,
    index_file: Path,
    append_str: str,
    prepend_str: str = "",
) -> None:
    """Write/Append string into a gallery header file.

    Parameters
    ----------
    header_file : Path
        The path to the example header file.
    index_file : Path
        The path to the output gallery index file.
    append_str : str
        The string to append to the gallery header file.
    prepend_str : str, optional
        The string to prepend to the gallery header file.

    """
    index_file = Path(index_file)
    header_file = Path(header_file)
    ensure_dir_exists(index_file.parent)
    if not index_file.exists():
        # copy and append the header file if not exists
        with index_file.open("w", encoding="utf-8") as dst:
            with header_file.open(encoding="utf-8") as src:
                content = f"{prepend_str}\n\n{src.read()}\n{append_str}"
            dst.write(content)
    else:
        # only append the string if the file exists
        with index_file.open("a", encoding="utf-8") as dst:
            dst.write(append_str)
