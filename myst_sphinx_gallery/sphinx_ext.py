# from myst_nb.sphinx_ import Parser
from sphinx.application import Sphinx

from .config import GalleryConfig
from .gallery import generate_gallery


def main(app: Sphinx):
    gallery_conf = app.config.myst_sphinx_gallery_config
    if gallery_conf is None:
        raise ValueError(
            "Please set `myst_sphinx_gallery_config` in your conf.py file. "
            "or directly pass a `GalleryConfig` instance to `generate_gallery`. "
            "See https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/multi_galleries.html "
            "for more information."
        )
    if not isinstance(gallery_conf, (GalleryConfig, dict)):
        raise ValueError(
            "Please set `myst_sphinx_gallery_config` to an instance of `GalleryConfig` "
            "or a dict of arguments to initialize `GalleryConfig`."
            "See https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/multi_galleries.html"
            "for more information."
        )
    generate_gallery(gallery_conf)


def sphinx_setup(app: Sphinx):
    app.add_config_value("myst_sphinx_gallery_config", None, "")
    app.connect("builder-inited", main)
