from pathlib import Path

import pytest

from myst_sphinx_gallery import gallery, gen_gallery


@pytest.fixture
def cwd():
    return Path(__file__).parent


@pytest.fixture
def examples_dir(cwd):
    return cwd.parent / "examples"


@pytest.fixture
def gallery_dir(cwd):
    return cwd / "_build" / "auto_examples"


@pytest.fixture
def example_header_file(examples_dir):
    return examples_dir / "02-alt_strategy_order" / "GALLERY_HEADER.rst"


def test_parse_config():
    pass


# def test_section(example_header_file, examples_dir, gallery_dir):
#     section = gallery.SectionGenerator(
#         example_header_file,
#         examples_dir,
#         gallery_dir,
#     )
#     section.convert()
#     print(section.toc)
#     print(section.grid)


def test_generate_gallery(examples_dir, gallery_dir):
    gen_gallery.generate_gallery(examples_dir, gallery_dir)
    assert (gallery_dir / "index.rst").exists()


def test_get_rst_title(example_header_file):
    title = gallery.get_rst_title(example_header_file)
    assert title == "Example Files without Number"
