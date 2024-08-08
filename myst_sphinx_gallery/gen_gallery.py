"""
Sphinx extension to generate a gallery from Jupyter notebooks, MyST markdown, and reStructuredText files. 
"""

from __future__ import annotations

from pathlib import Path

from sphinx.application import Sphinx

from .__init__ import __version__
from .gallery import generate_gallery

DEFAULT_GALLERY_CONF = {
    "thumbnail_strategy": "last",
    "notebook_thumbnail_strategy": "markdown",
    "default_thumbnail_file": "_static/thumbnail.png",
    "examples_dirs": "../../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
}


def main(app: Sphinx):

    gallery_conf = app.config.myst_sphinx_gallery_options

    src_dir = Path(app.builder.srcdir)
    gallery_dir = (src_dir / gallery_conf["gallery_dirs"]).resolve()
    examples_dir = (src_dir / gallery_conf["examples_dirs"]).resolve()

    generate_gallery(examples_dir, gallery_dir)


def setup(app: Sphinx):
    # ! This function not working now
    app.add_config_value("myst_sphinx_gallery_options", DEFAULT_GALLERY_CONF, "")

    # app.connect("config-inited", parse_config)
    app.connect("builder-inited", main)

    return {
        "version": __version__,
        "parallel_read_safe": False,
        "parallel_write_safe": False,
    }
