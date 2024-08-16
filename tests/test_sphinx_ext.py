from unittest.mock import Mock, patch

import pytest
from sphinx.application import Sphinx

from myst_sphinx_gallery.config import GalleryConfig
from myst_sphinx_gallery.gallery import generate_gallery
from myst_sphinx_gallery.sphinx_ext import main


class MockConfig:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockApp(Sphinx):
    config = MockConfig(myst_sphinx_gallery_config=Mock(spec=GalleryConfig))


@pytest.fixture
def app():
    app = Mock(spec=MockApp)
    return app


def test_main_no_config(app):
    app.config.myst_sphinx_gallery_config = None
    with pytest.raises(
        ValueError,
        match="Please set `myst_sphinx_gallery_config` in your conf.py file.",
    ):
        main(app)


def test_main_invalid_config_type(app):
    app.config.myst_sphinx_gallery_config = "invalid_config"
    with pytest.raises(
        ValueError,
        match="Please set `myst_sphinx_gallery_config` to an instance of `GalleryConfig`",
    ):
        main(app)


def test_main_valid_gallery_config(app):
    gallery_conf = Mock(spec=GalleryConfig)
    app.config.myst_sphinx_gallery_config = gallery_conf
    with patch(
        "myst_sphinx_gallery.sphinx_ext.generate_gallery"
    ) as mock_generate_gallery:
        main(app)
        mock_generate_gallery.assert_called_once_with(gallery_conf)


def test_main_valid_dict_config(app):
    gallery_conf = {"key": "value"}
    app.config.myst_sphinx_gallery_config = gallery_conf
    with patch(
        "myst_sphinx_gallery.sphinx_ext.generate_gallery"
    ) as mock_generate_gallery:
        main(app)
        mock_generate_gallery.assert_called_once_with(gallery_conf)
