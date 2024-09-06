from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from sphinx.application import Sphinx

from myst_sphinx_gallery.config import GalleryConfig
from myst_sphinx_gallery.sphinx_ext import cleanup_thumbnail, main


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
    gallery_conf = {
        "examples_dirs": "examples",
        "gallery_dirs": "galleries",
        "root_dir": "/root",
    }
    app.config.myst_sphinx_gallery_config = gallery_conf
    with patch(
        "myst_sphinx_gallery.sphinx_ext.generate_gallery"
    ) as mock_generate_gallery:
        main(app)
        mock_generate_gallery.assert_called_once_with(gallery_conf)


class TestCleanupThumbnail:
    def test_cleanup_thumbnail(self, tmp_path):
        srcdir = tmp_path
        thumb_dir = srcdir / "myst_sphinx_gallery_thumbs"
        thumb_dir.mkdir()
        assert thumb_dir.exists()
        # Arrange
        app = Mock()
        app.srcdir = srcdir
        app.config = Mock()
        app.config.myst_sphinx_gallery_config = Mock()
        app.config.myst_sphinx_gallery_config.remove_thumbnail_after_build = True

        # Act
        cleanup_thumbnail(app, None)

        assert not thumb_dir.exists()

    def test_cleanup_thumbnail_no_removal(self, tmp_path):
        srcdir = tmp_path
        thumb_dir = srcdir / "myst_sphinx_gallery_thumbs"
        thumb_dir.mkdir(parents=True)
        assert thumb_dir.exists()
        # Arrange
        app = Mock()
        app.srcdir = srcdir
        app.config = Mock()
        app.config.myst_sphinx_gallery_config = Mock()
        app.config.myst_sphinx_gallery_config.remove_thumbnail_after_build = False

        # Act
        cleanup_thumbnail(app, None)

        assert thumb_dir.exists()
