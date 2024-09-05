"""Configuration classes for the gallery."""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .grid import Grid, GridItemCard, TocTree
from .utils import abs_path


@dataclass
class FilesConfig:
    """Set different thumbnail configuration for different files."""

    named_config: dict[str, GalleryThumbnailConfig] = field(default_factory=dict)
    """A dictionary giving the names for different configurations.

    The key and value of the dictionary are the names and configurations of the
    thumbnail configurations, respectively: {name_of_config: GalleryThumbnailConfig()}
    """

    files_config: dict[str, list[str]] = field(default_factory=dict)
    """The configurations for different files.

    .. note::
        1. The key of the dictionary is a name string of the configurations in
           :attr:`named_config`, and the value is a list of paths to the files:
           {name_of_config: [path_to_file1, path_to_file2, ...]}
        2. The paths are relative to the ``conf.py`` file.
    """

    def __post_init__(self) -> None:
        """Post initialization function to check the configurations."""
        files_config_map = {}
        for config_name, files in self.files_config.items():
            if config_name not in self.named_config:
                msg = f"Configuration {config_name} is not found in named_config."
                warnings.warn(msg, stacklevel=2)
            for file_path in files:
                files_config_map[file_path] = self.named_config[config_name]

        self.files_config_map = files_config_map

    def to_dict(self) -> dict:
        """Convert the configuration to a dictionary."""
        return self.__dict__.copy()

    def get(self, file_path: str) -> GalleryThumbnailConfig:
        """Get the configuration for a file path."""
        return self.files_config_map.get(file_path, GalleryThumbnailConfig())


@dataclass
class ThumbnailConfig:
    """Configuration to setup the :class:`~myst_sphinx_gallery.images.Thumbnail` class.

    This class is used to specify the parameters to create a thumbnail from an image.
    """

    ref_size: tuple[int, int] = (320, 224)
    """the reference size of the thumbnail image for output."""

    operation: Literal["thumbnail", "contain", "cover", "fit", "pad"] = "pad"
    """The operation to perform on the image.

    See the Pillow documentation for more information:
    `<https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#relative-resizing>`_
    """

    operation_kwargs: dict[str, int] = field(default_factory=dict)
    """The parameters passed to the operation function."""

    max_animation_frames: int = 100
    """The maximum number of frames to extract from an animated image.
    If the image has more frames, will sample the frames uniformly.

    .. tip::
        If you want to make the thumbnail of animated images to be static images,
        you can set this value to 1.

    .. versionadded:: 0.2.2
    """

    quality_static: int = 80
    """The quality of the static image thumbnail.

    .. versionadded:: 0.2.1
    """

    quality_animated: int = 50  # small quality for smaller size of animated thumbnail
    """The quality of the animated image thumbnail.

    .. versionadded:: 0.2.1
    """

    save_kwargs: dict[str, int] = field(default_factory=dict)
    """The parameters passed to save function for the thumbnail image.

    See the Pillow documentation for more information:
    `<https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp-saving>`_

    .. note::
        The ``quality`` of the saved image is suggested to be set by the
        :attr:`quality_static` and :attr:`quality_animated` attributes
        separately.
    """

    def to_dict(self) -> dict:
        """Convert the configuration to a dictionary."""
        return self.__dict__.copy()


@dataclass
class GalleryConfig:
    """Configurations to generate the gallery from examples.

    Examples
    --------
    if you are using this configuration in ``conf.py``, you can initialize
    the configuration as follows::

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig

        gallery_config = GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
        )

    """

    examples_dirs: Path | str | list[Path | str] | None = None
    """The directories containing the example scripts. There must be a
    ``GALLERY_HEADER.rst`` file in each of these directories.

    .. note::
        1. The paths are relative to the root directory :attr:`root_dir`.
        2. If a list of paths is provided, the number of paths must match
           the number of paths in :attr:`gallery_dirs`.

    .. versionchanged:: 0.3.0
        Can be ``None`` for pure configuration, which not generating the gallery.
    """

    gallery_dirs: Path | str | list[Path | str] | None = None
    """The directories where the gallery output will be saved.

    .. note::
        1. The paths are relative to the root directory :attr:`root_dir`.
        2. If a list of paths is provided, the number of paths must match t
           number of paths in :attr:`examples_dirs`.

    .. versionchanged:: 0.3.0
        Can be ``None`` for pure configuration, which not generating the gallery.
    """

    root_dir: Path | str | None = None
    """The root directory for any relative paths in this configuration.

    .. tip::
        You can use the ``__file__`` variable to get the path to the
        current file if you are using this configuration in ``conf.py``.
        For example, ``Path(__file__).parent`` is the root directory in this case.

    .. versionchanged:: 0.3.0
        Can be ``None`` for pure configuration, which not generating the gallery.
    """

    thumbnail_strategy: Literal["first", "last"] = "last"
    """The strategy to use for selecting the thumbnail image for each example
    if multiple images are candidates.
    """

    notebook_thumbnail_strategy: Literal["markdown", "code"] = "markdown"
    """The strategy to use for selecting the thumbnail image for jupyter notebook,
    if both ``markdown`` and ``code`` cells contain images.
    """

    default_thumbnail_file: Path | str | None = None
    """The path to the default thumbnail image file.
    If no thumbnail image is found for an example, this image will be used.
    If None, a default thumbnail image in this package will be used.
    """

    thumbnail_config: ThumbnailConfig = field(default_factory=ThumbnailConfig)
    """The configuration for the thumbnail image."""

    remove_thumbnail_after_build: bool = True
    """Whether to remove the thumbnail image after building the gallery."""

    base_gallery: bool = False
    """Whether the examples are a base gallery.

    .. tip::
        You can use the ``base-gallery`` directive alternatively.

    .. versionadded:: 0.3.0
    """

    target_prefix: str = "example_"
    """The prefix to use for the target names of the gallery files.

    .. versionadded:: 0.2.1
    """

    toc_tree: TocTree = field(default_factory=TocTree)
    """A instance of :class:`~myst_sphinx_gallery.TocTree` class to create
    a table of content for gallery. Currently, no additional options are supported.

    .. versionchanged:: 0.3.0
        This parameter is not suggested to be used  by user. It will only be
        internally used by program.
    """

    grid: Grid = field(default_factory=Grid)
    """A instance of :class:`~myst_sphinx_gallery.Grid` class for gallery.
    You can customize the grid layout using this configuration.

    .. versionchanged:: 0.3.0
        This parameter is not suggested to be used by user. It will only be
        internally used by program.
    """

    grid_item_card: GridItemCard = field(default_factory=GridItemCard)
    """A instance of :class:`~myst_sphinx_gallery.GridItemCard` class for gallery.
    You can customize he grid item card using this configuration.

    .. versionchanged:: 0.3.0
        This parameter is not suggested to be used by user. It will only be
        internally used by program.
    """

    def __post_init__(self) -> None:
        """Post initialization function to format the configurations."""
        if self.examples_dirs is not None and self.gallery_dirs is not None:
            if isinstance(self.examples_dirs, (Path, str)):
                self.examples_dirs = [self.examples_dirs]
            if isinstance(self.gallery_dirs, (Path, str)):
                self.gallery_dirs = [self.gallery_dirs]

            if len(self.examples_dirs) != len(self.gallery_dirs):
                msg = "The number of paths in examples_dirs and gallery_dirs must match"
                raise ValueError(msg)

            self.examples_dirs = [self.abs_path(d) for d in self.examples_dirs]
            self.gallery_dirs = [self.abs_path(d) for d in self.gallery_dirs]

            if self.default_thumbnail_file is not None:
                self.default_thumbnail_file = self.abs_path(self.default_thumbnail_file)

        # clear the items in toc_tree, grid, and grid_item_card, keeping the options
        self.toc_tree = self.toc_tree.copy()
        self.grid = self.grid.copy()
        self.grid_item_card = self.grid_item_card.copy()

    def abs_path(self, path: Path | str) -> Path:
        """Convert a path to an absolute path using the root directory."""
        return abs_path(path, self.root_dir)

    def to_dict(self) -> dict:
        """Convert the configuration to a dictionary."""
        return self.__dict__.copy()


@dataclass
class GalleryThumbnailConfig:
    """Configurations to generate the gallery from examples.

    Examples
    --------
    if you are using this configuration in ``conf.py``, you can initialize
    the configuration as follows::

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig

        gallery_config = GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
        )

    """

    thumbnail_strategy: Literal["first", "last"] = "last"
    """The strategy to use for selecting the thumbnail image for each example
    if multiple images are candidates.
    """

    notebook_thumbnail_strategy: Literal["markdown", "code"] = "markdown"
    """The strategy to use for selecting the thumbnail image for jupyter notebook,
    if both ``markdown`` and ``code`` cells contain images.
    """

    default_thumbnail_file: Path | str | None = None
    """The path to the default thumbnail image file.
    If no thumbnail image is found for an example, this image will be used.
    If None, a default thumbnail image in this package will be used.
    """

    thumbnail_config: ThumbnailConfig = field(default_factory=ThumbnailConfig)
    """The configuration for the thumbnail image."""

    def to_dict(self) -> dict:
        """Convert the configuration to a dictionary."""
        return self.__dict__.copy()
