from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .grid import Grid, GridItemCard, TocTree
from .utils import abs_path


@dataclass
class ThumbnailConfig:
    """Configuration to setup the :class:`~myst_sphinx_gallery.images.Thumbnail`
    class. This class is used to specify the parameters to create a thumbnail
    from an image.
    """

    #: the reference size of the thumbnail image for output.
    ref_size: tuple[int, int] = (320, 224)

    #: The operation to perform on the image. See the Pillow documentation for
    #: more information: `<https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#relative-resizing>`_
    operation: Literal["thumbnail", "contain", "cover", "fit", "pad"] = "pad"

    #: The parameters passed to the operation function.
    operation_kwargs: dict[str, int] = field(default_factory=dict)

    #: The maximum number of frames to extract from an animated image.
    #: If the image has more frames, will sample the frames uniformly.
    #:
    #: .. tip::
    #:    If you want to make the thumbnail of animated images to be static images,
    #:    you can set this value to 1.
    #:
    #: .. versionadded:: 0.2.2
    max_animation_frames: int = 100

    #: The quality of the static image thumbnail.
    #:
    #: .. versionadded:: 0.2.1
    quality_static: int = 80

    #: The quality of the animated image thumbnail.
    #:
    #: .. versionadded:: 0.2.1
    quality_animated: int = 50  # small quality for smaller size of animated thumbnail

    #: The parameters passed to save function for the thumbnail image.
    #: See the Pillow documentation for more information:
    #: `<https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp-saving>`_
    #:
    #: .. note::
    #:    The ``quality`` of the saved image is suggested to be set by the
    #:    :attr:`quality_static` and :attr:`quality_animated` attributes
    #:    separately.
    save_kwargs: dict[str, int] = field(default_factory=dict)

    def to_dict(self):
        """Convert the configuration to a dictionary"""
        return self.__dict__.copy()


@dataclass
class GalleryConfig:
    """Configurations for MyST Sphinx Gallery

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

    #: The directories containing the example scripts. There must be a
    #: ``GALLERY_HEADER.rst`` file in each of these directories.
    #:
    #: .. note::
    #:
    #:    1. The paths are relative to the root directory :attr:`root_dir`.
    #:    2. If a list of paths is provided, the number of paths must match
    #:       the number of paths in :attr:`gallery_dirs`.
    examples_dirs: Path | str | list[Path | str]

    #: The directories where the gallery output will be saved.
    #:
    #: .. note::
    #:
    #:    1. The paths are relative to the root directory :attr:`root_dir`.
    #:    2. If a list of paths is provided, the number of paths must match the
    #:       number of paths in :attr:`examples_dirs`.
    gallery_dirs: Path | str | list[Path | str]

    #: The root directory for any relative paths in this configuration.
    #:
    #: .. tip::
    #:    You can use the ``__file__`` variable to get the path to the
    #:    current file if you are using this configuration in ``conf.py``.
    #:    For example, ``Path(__file__).parent`` is the root directory in this case.
    root_dir: Path | str

    #: The strategy to use for selecting the thumbnail image for each example
    #: if multiple images are candidates.
    thumbnail_strategy: Literal["first", "last"] = "last"

    #: The strategy to use for selecting the thumbnail image for jupyter notebook,
    #: if both a ``markdown`` cell and ``code`` cell are present.
    notebook_thumbnail_strategy: Literal["markdown", "code"] = "markdown"

    #: The path to the default thumbnail image file.
    #: If no thumbnail image is found for an example, this image will be used.
    #: If None, a default thumbnail image in this package will be used.
    default_thumbnail_file: Path | str | None = None

    #: The configuration for the thumbnail image.
    thumbnail_config: ThumbnailConfig = field(default_factory=ThumbnailConfig)

    #: The prefix to use for the target names of the gallery files.
    #:
    #: .. versionadded:: 0.2.1
    target_prefix: str = "example_"

    #: A instance of :class:`~myst_sphinx_gallery.TocTree` class to create
    #: a table of content for gallery. Currently, no additional options are supported.
    toc_tree: TocTree = field(default_factory=TocTree)

    #: A instance of :class:`~myst_sphinx_gallery.Grid` class for gallery.
    #: You can customize the grid layout using this configuration.
    grid: Grid = field(default_factory=Grid)

    #: A instance of :class:`~myst_sphinx_gallery.GridItemCard` class for gallery.
    #: You can customize he grid item card using this configuration.
    grid_item_card: GridItemCard = field(default_factory=GridItemCard)

    def __post_init__(self):
        if isinstance(self.examples_dirs, (Path, str)):
            self.examples_dirs = [self.examples_dirs]
        if isinstance(self.gallery_dirs, (Path, str)):
            self.gallery_dirs = [self.gallery_dirs]

        if len(self.examples_dirs) != len(self.gallery_dirs):
            raise ValueError(
                "The number of paths in examples_dirs and gallery_dirs must match"
            )

        self.examples_dirs = [self.abs_path(d) for d in self.examples_dirs]
        self.gallery_dirs = [self.abs_path(d) for d in self.gallery_dirs]

        if self.default_thumbnail_file is not None:
            self.default_thumbnail_file = self.abs_path(self.default_thumbnail_file)

        # clear the items in toc_tree, grid, and grid_item_card, keeping the options
        self.toc_tree = self.toc_tree.copy()
        self.grid = self.grid.copy()
        self.grid_item_card = self.grid_item_card.copy()

    def abs_path(self, path: Path | str) -> Path:
        """Convert a path to an absolute path using the root directory"""
        return abs_path(path, self.root_dir)

    def to_dict(self):
        """Convert the configuration to a dictionary"""
        return self.__dict__.copy()
