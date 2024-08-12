from pathlib import Path

import pytest

from myst_sphinx_gallery import GalleryConfig, ThumbnailConfig


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


class TestThumbnailConfig:
    def test_thumbnail_config(self):
        config = ThumbnailConfig(
            ref_size=(640, 480),
            operation="cover",
            operation_kwargs={"quality": 95},
            save_kwargs={"optimize": True},
        )
        assert config.ref_size == (640, 480)
        assert config.operation == "cover"
        assert config.operation_kwargs == {"quality": 95}
        assert config.save_kwargs == {"optimize": True}

    def test_thumbnail_config_defaults(self):
        config = ThumbnailConfig()
        assert config.ref_size == (320, 224)
        assert config.operation == "pad"
        assert config.operation_kwargs == {}
        assert config.save_kwargs == {}

    def test_thumbnail_config_to_dict(self):
        config = ThumbnailConfig(
            ref_size=(640, 480),
            operation="cover",
            operation_kwargs={"quality": 95},
            save_kwargs={"optimize": True},
        )
        config_dict = config.to_dict()
        assert config_dict["ref_size"] == (640, 480)
        assert config_dict["operation"] == "cover"
        assert config_dict["operation_kwargs"] == {"quality": 95}
        assert config_dict["save_kwargs"] == {"optimize": True}


class TestGalleryConfig:
    def test_gallery_config_single_path(self, cwd):
        config = GalleryConfig(
            examples_dirs="examples",
            gallery_dirs="auto_examples",
            root_dir=cwd,
            notebook_thumbnail_strategy="code",
            default_thumbnail_file="_static/default_thumbnail.png",
        )
        assert config.examples_dirs == [cwd / "examples"]
        assert config.gallery_dirs == [cwd / "auto_examples"]
        assert config.root_dir == cwd
        assert config.default_thumbnail_file == cwd / "_static/default_thumbnail.png"

    def test_gallery_config_multiple_paths(self, cwd):
        config = GalleryConfig(
            examples_dirs=["examples1", "examples2"],
            gallery_dirs=["auto_examples1", "auto_examples2"],
            root_dir=cwd,
            notebook_thumbnail_strategy="code",
            default_thumbnail_file="_static/default_thumbnail.png",
        )
        assert config.examples_dirs == [cwd / "examples1", cwd / "examples2"]
        assert config.gallery_dirs == [cwd / "auto_examples1", cwd / "auto_examples2"]
        assert config.root_dir == cwd
        assert config.default_thumbnail_file == cwd / "_static/default_thumbnail.png"

    def test_gallery_config_invalid_paths(self, cwd):
        with pytest.raises(ValueError):
            GalleryConfig(
                examples_dirs=["examples1"],
                gallery_dirs=["auto_examples1", "auto_examples2"],
                root_dir=cwd,
                notebook_thumbnail_strategy="code",
                default_thumbnail_file="_static/default_thumbnail.png",
            )

    def test_gallery_config_abs_path(self, cwd):
        config = GalleryConfig(
            examples_dirs="examples",
            gallery_dirs="auto_examples",
            root_dir=cwd,
            notebook_thumbnail_strategy="code",
            default_thumbnail_file="_static/default_thumbnail.png",
        )
        assert config.abs_path("some_path") == (cwd / "some_path").resolve()

    def test_gallery_config_to_dict(self, cwd):
        config = GalleryConfig(
            examples_dirs="examples",
            gallery_dirs="auto_examples",
            root_dir=cwd,
            notebook_thumbnail_strategy="code",
            default_thumbnail_file="_static/default_thumbnail.png",
        )
        config_dict = config.to_dict()
        assert config_dict["examples_dirs"] == [cwd / "examples"]
        assert config_dict["gallery_dirs"] == [cwd / "auto_examples"]
        assert config_dict["root_dir"] == cwd
        assert config_dict["notebook_thumbnail_strategy"] == "code"
        assert (
            config_dict["default_thumbnail_file"]
            == cwd / "_static/default_thumbnail.png"
        )
