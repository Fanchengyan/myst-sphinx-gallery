"""Setup the Sphinx extension for MyST-Sphinx-Gallery."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from docutils.nodes import NodeVisitor

from .config import GalleryConfig
from .directives import (
    BaseGallery,
    GalleryDirective,
    RefGalleryDirective,
    card_col_node,
)
from .gallery import generate_gallery
from .utils import gallery_static_path, safe_remove_dir

if TYPE_CHECKING:
    from docutils import nodes
    from sphinx.application import Sphinx


class CardNodeHTMLTranslator(NodeVisitor):
    """HTML translator for CardNode."""

    def visit_card_node(self, node: nodes.Node) -> None:
        """Visit CardNode."""
        tooltip = node.get("tooltip", "")
        self.body.append(self.starttag(node, "div", "", tooltip=tooltip))

    def depart_card_node(self, node: nodes.Node) -> None:  # noqa: ARG002
        """Depart CardNode."""
        self.body.append("</div>")


def cleanup_thumbnail(
    app: Sphinx,
    exception: Exception,  # noqa: ARG001
) -> None:
    """Remove the doctrees directory.

    If the build is successful, the doctrees directory is removed.
    """
    remove_thumbnail = True
    config = app.config
    if (
        hasattr(config, "myst_sphinx_gallery_config")
        and config.myst_sphinx_gallery_config
    ):
        remove_thumbnail = (
            config.myst_sphinx_gallery_config.remove_thumbnail_after_build
        )
    if remove_thumbnail:
        doctrees_dirs = list(Path(app.srcdir).rglob("myst_sphinx_gallery_thumbs"))
        for doctrees_dir in doctrees_dirs:
            safe_remove_dir(doctrees_dir)


def config_inited(app: Sphinx) -> None:
    """Append path to packaged static files to `html_static_path`."""
    path = str(gallery_static_path())
    if path not in app.config.html_static_path:
        app.config.html_static_path.append(path)
    app.add_css_file("myst_sphinx_gallery.css", priority=501)


def main(app: Sphinx) -> None:
    """Generate gallery."""
    config = app.config
    if hasattr(config, "myst_sphinx_gallery_config"):
        gallery_conf = app.config.myst_sphinx_gallery_config
        if gallery_conf is not None:
            msg = (
                "Please set `myst_sphinx_gallery_config` to an instance of "
                "`GalleryConfig` or a dict of arguments to initialize `GalleryConfig`."
                "See https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/multi_galleries.html"
                "for more information."
            )
            if not isinstance(gallery_conf, (GalleryConfig, dict)):
                raise ValueError(msg)
            if (
                (  # skip build if any of the required directories are not set
                    isinstance(gallery_conf, GalleryConfig)
                    and (
                        gallery_conf.examples_dirs is None
                        or gallery_conf.gallery_dirs is None
                        or gallery_conf.root_dir is None
                    )
                )
                or isinstance(gallery_conf, dict)
                and (
                    gallery_conf.get("examples_dirs") is None
                    or gallery_conf.get("gallery_dirs") is None
                    or gallery_conf.get("root_dir") is None
                )
            ):
                return
            generate_gallery(gallery_conf)


def sphinx_setup(app: Sphinx) -> None:
    """Actions to setup the Sphinx extension."""
    app.add_directive("ref-gallery", RefGalleryDirective)
    app.add_directive("base-gallery", BaseGallery)
    app.add_directive("gallery", GalleryDirective)
    app.add_node(
        card_col_node,
        html=(
            CardNodeHTMLTranslator.visit_card_node,
            CardNodeHTMLTranslator.depart_card_node,
        ),
    )

    app.setup_extension("sphinx_design")
    app.add_config_value("myst_sphinx_gallery_config", None, "")
    app.add_config_value("myst_sphinx_gallery_files_config", None, "")
    app.connect("builder-inited", main)
    app.connect("builder-inited", config_inited)
    app.connect("build-finished", cleanup_thumbnail)
