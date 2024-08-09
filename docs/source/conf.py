# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "MyST Sphinx Gallery"
copyright = "2024, Fan Chengyan (Fancy)"
author = "Fan Chengyan (Fancy)"

# -- MyST Sphinx Gallery Configuration ---------------------------------------
from pathlib import Path

from myst_sphinx_gallery import GalleryConfig, __version__, generate_gallery

myst_sphinx_gallery_config = GalleryConfig(
    examples_dirs="../../examples",
    gallery_dirs="auto_examples",
    root_dir=Path(__file__).parent,
    notebook_thumbnail_strategy="code",
)
generate_gallery(myst_sphinx_gallery_config)

release = f"v{__version__}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "myst_nb",
    # "myst_sphinx_gallery.gen_gallery",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".myst": "myst-nb",
}
myst_enable_extensions = ["colon_fence"]
myst_url_schemes = ["http", "https", "mailto"]
suppress_warnings = ["mystnb.unknown_mime_type"]
nb_execution_mode = "off"
autodoc_inherit_docstrings = True
# templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo/logo.svg"
html_favicon = "_static/logo/logo-square.svg"
html_theme_options = {
    "show_toc_level": 2,
    "show_nav_level": 2,
    "header_links_before_dropdown": 10,
    "use_edit_page_button": True,
    "pygments_light_style": "default",
    "pygments_dark_style": "fruity",
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Fanchengyan/myst-sphinx-gallery",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/myst-sphinx-gallery",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
}

video_enforce_extra_source = True

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    ":show-inheritance:": True,
}
html_context = {
    "github_url": "https://github.com",
    "github_user": "Fanchengyan",
    "github_repo": "myst-sphinx-gallery",
    "github_version": "main",
    "doc_path": "docs/source",
}


# connect docs in other projects
intersphinx_mapping = {
    "python": (
        "https://docs.python.org/3",
        "https://docs.python.org/3/objects.inv",
    ),
    "myst-parser": (
        "https://myst-parser.readthedocs.io/en/latest",
        "https://myst-parser.readthedocs.io/en/latest/objects.inv",
    ),
}


# -- myst_sphinx_gallery package ----------------------------------------------------------
import os
import sys

# Location of Sphinx files
sys.path.insert(0, os.path.abspath("./../.."))
