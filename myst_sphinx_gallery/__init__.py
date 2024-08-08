"""
MyST Sphinx Gallery
===================

"""

from pathlib import Path

from sphinx.application import Sphinx

from .gallery import generate_gallery

# dev versions should have "dev" in them, stable should not.
# doc/conf.py makes use of this to set the version drop-down.
# eg: "0.1.dev0", "0.1"
__version__ = "0.1"
