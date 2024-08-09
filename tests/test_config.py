from pathlib import Path

import pytest

from myst_sphinx_gallery import GalleryConfig


@pytest.fixture
def cwd():
    return Path(__file__).parent


@pytest.fixture
def config():
    return GalleryConfig(
        examples_dirs="../examples",
        gallery_dirs="auto_examples",
        root_dir=Path(__file__).parent,
        notebook_thumbnail_strategy="code",
        default_thumbnail_file="_static/default_thumbnail.png",
    )


def test_config_path(config, cwd):
    def abs_path(path, root_dir: Path):
        return (root_dir / path).resolve()

    print(f"config = {config}")
    assert config.examples_dirs == [abs_path("../examples", cwd)]
    assert config.gallery_dirs == [abs_path("auto_examples", cwd)]
    assert config.root_dir == cwd
    assert config.default_thumbnail_file == abs_path(
        "_static/default_thumbnail.png", cwd
    )
