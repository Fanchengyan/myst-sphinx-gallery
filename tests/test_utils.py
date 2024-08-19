from pathlib import Path

import pytest

from myst_sphinx_gallery.utils import abs_path, ensure_dir_exists, safe_remove_file

cwd = Path(__file__).parent

data_dir = cwd / "data"
out_dir = cwd / "_build/thumbnails"


@pytest.fixture
def root_dir():
    return Path("/root")


class TestAbsPath:
    def test_abs_path_relative(self, root_dir):
        relative_path = "subdir/file.txt"
        expected = (root_dir / relative_path).resolve()
        assert abs_path(relative_path, root_dir) == expected

    def test_abs_path_absolute(self, root_dir):
        absolute_path = "/subdir/file.txt"
        expected = (root_dir / f".{absolute_path}").resolve()
        assert abs_path(absolute_path, root_dir) == expected

    def test_abs_path_different_root(self):
        relative_path = "subdir/file.txt"
        new_root_dir = Path("/new_root")
        expected = (new_root_dir / relative_path).resolve()
        assert abs_path(relative_path, new_root_dir) == expected

    def test_abs_path_special_characters(self, root_dir):
        special_path = "subdir/../file.txt"
        expected = (root_dir / special_path).resolve()
        assert abs_path(special_path, root_dir) == expected


class TestEnsureDirExists:
    def test_ensure_dir_exists(self):
        ensure_dir_exists(out_dir)
        assert out_dir.is_dir()

    def test_remove_and_create(self):
        if out_dir.exists():
            files = list(out_dir.glob("*"))
            for file in files:
                safe_remove_file(file)
                safe_remove_file(file)  # test removing non-existent file
            out_dir.rmdir()
        ensure_dir_exists(out_dir)
        assert out_dir.is_dir()
