"""
Sphinx extension to generate a gallery from Jupyter notebooks, MyST markdown, and reStructuredText files. 
"""

from __future__ import annotations

import os
import shutil
import warnings
from pathlib import Path

from .gallery import GalleryGenerator

DEFAULT_GALLERY_CONF = {
    "thumbnail_strategy": "last",
    "thumbnail_strategy_notebook": "markdown",
    "default_thumb_file": "_static/thumbnail.png",
    "examples_dirs": "../../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
}


def main(app):
    gallery_conf = app.config.myst_sphinx_gallery_options
    if not isinstance(gallery_conf, dict):
        raise ValueError("myst_sphinx_gallery_options must be a dictionary")
    src_dir = Path(app.builder.srcdir)
    gallery_dir = (src_dir / gallery_conf["gallery_dirs"]).resolve()
    examples_dir = (src_dir / gallery_conf["examples_dirs"]).resolve()


def generate_gallery(examples_dir, gallery_dir):
    """Generate the gallery from the examples directory."""
    shutil.rmtree(gallery_dir, ignore_errors=True)

    gallery = GalleryGenerator(
        examples_dir,
        gallery_dir,
    )
    gallery.convert()


def setup(app):
    app.add_config_value("myst_sphinx_gallery_options", DEFAULT_GALLERY_CONF, "html")

    # app.connect("config-inited", parse_config)
    app.connect("builder-inited", main, priority=100)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
