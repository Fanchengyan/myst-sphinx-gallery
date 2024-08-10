from pathlib import Path

import pytest

from myst_sphinx_gallery import gallery, generate_gallery, GalleryConfig


@pytest.fixture
def cwd():
    return Path(__file__).parent


@pytest.fixture
def examples_dir(cwd):
    return cwd.parent / "examples"


@pytest.fixture
def gallery_dir(cwd):
    # return cwd / "_build" / "auto_examples"
    return cwd.parent / "docs" / "source" / "auto_examples"


@pytest.fixture
def example_header_file(examples_dir):
    return examples_dir / "GALLERY_HEADER.rst"


@pytest.fixture
def gallery_config(examples_dir, gallery_dir, cwd):
    return GalleryConfig(
        examples_dirs=[examples_dir],
        gallery_dirs=[gallery_dir],
        root_dir=cwd.parent,
    )


def test_generate_gallery(gallery_config):
    generate_gallery(gallery_config)
    index_file = gallery_config.gallery_dirs[0] / "index.rst"
    print(index_file)
    assert index_file.exists()


def test_get_rst_title(example_header_file):
    title = gallery.get_rst_title(example_header_file)
    assert title == "Gallery Example"
