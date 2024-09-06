"""
MyST Sphinx Gallery
===================

A Sphinx extension for generating a gallery from Jupyter notebooks, markdown and
reStructuredText files.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sphinx.util import logging

from .config import FilesConfig, GalleryConfig, GalleryThumbnailConfig, ThumbnailConfig
from .gallery import generate_gallery
from .grid import Grid, GridItemCard, TocTree
from .images import Thumbnail

if TYPE_CHECKING:
    from sphinx.application import Sphinx

logger = logging.getLogger("myst-sphinx-gallery")

# dev versions should have "dev" in them, stable should not.
# doc/conf.py makes use of this to set the version drop-down.
# eg: "0.1.dev0", "0.1"
__version__ = "0.3.0"


def setup(app: Sphinx) -> dict:
    """Set up the MyST-Sphinx-Gallery extension."""
    from .sphinx_ext import sphinx_setup

    sphinx_setup(app)

    return {
        "version": __version__,
        "parallel_read_safe": False,
        "parallel_write_safe": False,
    }
