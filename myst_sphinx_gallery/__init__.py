"""
MyST Sphinx Gallery
===================

"""

from sphinx.application import Sphinx

from .config import GalleryConfig, ThumbnailConfig
from .gallery import generate_gallery
from .grid import Grid, GridItemCard, TocTree
from .images import Thumbnail

# dev versions should have "dev" in them, stable should not.
# doc/conf.py makes use of this to set the version drop-down.
# eg: "0.1.dev0", "0.1"
__version__ = "0.2.2"


def setup(app: Sphinx):
    from .sphinx_ext import sphinx_setup

    sphinx_setup(app)

    return {
        "version": __version__,
        "parallel_read_safe": False,
        "parallel_write_safe": False,
    }
