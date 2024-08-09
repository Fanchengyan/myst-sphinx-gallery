from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


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
    #:    1. If the paths are relative, ``root_dir`` must be provided.
    #:    2. If a list of paths is provided, the number of paths must match
    #:       the number of paths in ``gallery_dirs``.
    examples_dirs: Path | str | list[Path | str]

    #: The directories where the gallery output will be saved.
    #:
    #: .. note::
    #:
    #:    1. If the paths are relative, ``root_dir`` must be provided.
    #:    2. If a list of paths is provided, the number of paths must match the
    #:       number of paths in ``example_dirs``.
    gallery_dirs: Path | str | list[Path | str]

    #: The root directory for any relative paths in this configuration.
    #:
    #: .. important::
    #:    This is must be provided if the paths in ``examples_dirs`` and
    #:    ``gallery_dirs`` are relative.
    #:
    #: .. tip::
    #:    You can use the ``__file__`` variable to get the path to the
    #:    current file if you are using this configuration in ``conf.py``.
    #:    For example, ``Path(__file__).parent`` is the root directory in this case.
    root_dir: Path | str | None = None

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

    def __post_init__(self):
        if isinstance(self.examples_dirs, (Path, str)):
            self.examples_dirs = [self.examples_dirs]
        if isinstance(self.gallery_dirs, (Path, str)):
            self.gallery_dirs = [self.gallery_dirs]

        if len(self.examples_dirs) != len(self.gallery_dirs):
            raise ValueError(
                "The number of paths in examples_dirs and gallery_dirs must match"
            )

        if self.root_dir is None and any(
            Path(d).is_absolute() for d in self.examples_dirs + self.gallery_dirs
        ):
            raise ValueError(
                "root_dir must be provided if examples_dirs or gallery_dirs are absolute paths"
            )

        self.examples_dirs = [self.abs_path(d) for d in self.examples_dirs]
        self.gallery_dirs = [self.abs_path(d) for d in self.gallery_dirs]

        if self.default_thumbnail_file is not None:
            self.default_thumbnail_file = self.abs_path(self.default_thumbnail_file)

    def abs_path(self, path: Path | str) -> Path:
        """Convert a path to an absolute path using the root directory"""
        path = Path(path)
        if not path.is_absolute():
            path = (self.root_dir / path).resolve()
        return path

    def to_dict(self):
        """Convert the configuration to a dictionary"""
        return self.__dict__.copy()
