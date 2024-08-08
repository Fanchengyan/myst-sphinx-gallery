"""
MyST Sphinx Gallery
===================

"""

from pathlib import Path

from .gallery import generate_gallery

# dev versions should have "dev" in them, stable should not.
# doc/conf.py makes use of this to set the version drop-down.
# eg: "0.1.dev0", "0.1"
__version__ = "0.1"


def gallery_path_static():
    """Returns path to packaged static files"""
    return Path(__file__).parent / "_static"
