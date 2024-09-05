from pathlib import Path

import pytest

from myst_sphinx_gallery import ThumbnailConfig
from myst_sphinx_gallery.gallery import GalleryConfig, generate_gallery


@pytest.fixture
def cwd():
    """Return the conf.py directory."""
    return Path(__file__).parent


@pytest.fixture
def gallery_dir_thumbnail():
    return "../../tests/_build/auto_examples_thumbnail"


@pytest.fixture
def config(cwd):
    return GalleryConfig(
        examples_dirs="./data/examples",
        gallery_dirs="./_build/auto_examples",
        root_dir=cwd,
        thumbnail_strategy="first",
        notebook_thumbnail_strategy="markdown",
    )


@pytest.fixture
def config2(cwd):
    return GalleryConfig(
        examples_dirs="./data/examples",
        gallery_dirs="./_build/auto_examples",
        root_dir=cwd,
        base_gallery=True,
        thumbnail_strategy="first",
        notebook_thumbnail_strategy="markdown",
    )


@pytest.fixture
def config_thumbnail(gallery_dir_thumbnail, cwd):
    return GalleryConfig(
        examples_dirs="./data/examples",
        gallery_dirs="./_build/auto_examples",
        root_dir=cwd,
        thumbnail_strategy="first",
        notebook_thumbnail_strategy="markdown",
        thumbnail_config=ThumbnailConfig(
            ref_size=(224, 320),
            operation_kwargs={"color": "black"},
            save_kwargs={"quality": 100},
        ),
    )


def prrint_sep():
    print(150 * ">")


def test_generate_gallery(config):
    prrint_sep()
    print("config : ", config)
    generate_gallery(config)


def test_generate_gallery_section(config2):
    prrint_sep()
    print("config : ", config2)
    generate_gallery(config2)


def test_generate_gallery_thumbnail(config_thumbnail):
    prrint_sep()
    print("Generate the gallery with the thumbnail configuration")
    print("config for thumbnail : ", config_thumbnail)

    # Generate the gallery with the thumbnail configuration
    generate_gallery(config_thumbnail)

    prrint_sep()
    thumb_dir = config_thumbnail.gallery_dirs[0] / "myst_sphinx_gallery_thumbs"
    print(
        f">>> Processing thumbnail images are in {thumb_dir}\n"
        ">>> You can check whether the thumbnail images are generated with the black background in the padding area."
    )
    prrint_sep()
    print(
        f">>> Processing thumbnail images are in {thumb_dir}\n"
        ">>> You can check whether the thumbnail images are generated with the black background in the padding area."
    )
    prrint_sep()
