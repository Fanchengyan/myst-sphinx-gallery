"""
Sphinx extension to generate a gallery from Jupyter notebooks, MyST markdown, and reStructuredText files. 
"""

from __future__ import annotations

from pathlib import Path

from sphinx.application import Sphinx

from .__init__ import __version__
from .config import GalleryConfig
from .gallery import generate_gallery

Default_Gallery_Config = GalleryConfig(
    examples_dirs="../../examples",
    gallery_dirs="auto_examples",
    root_dir=Path(__file__).parent,
    notebook_thumbnail_strategy="code",
)


def main(app: Sphinx):

    gallery_conf = app.config.myst_sphinx_gallery_config
    print(gallery_conf)
    generate_gallery(gallery_conf)


def setup(app: Sphinx):
    # ! This function not working now
    # would raise Handler <function main at 0x106260ea0> for event 'builder-inited' threw an exception (exception: 'Values' object has no attribute 'env')
    # make: *** [html] Error 2
    app.add_config_value("myst_sphinx_gallery_config", Default_Gallery_Config, "")

    # app.connect("config-inited", parse_config)
    app.connect("builder-inited", main)

    return {
        "version": __version__,
        "parallel_read_safe": False,
        "parallel_write_safe": False,
    }
