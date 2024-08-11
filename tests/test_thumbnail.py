from pathlib import Path

import pytest
from PIL import Image

from myst_sphinx_gallery.images import Thumbnail

cwd = Path(__file__).parent

data_dir = cwd / "data"
out_dir = cwd / "_build/thumbnails"

images = list(data_dir.glob("*.gif"))

png_files = list(data_dir.glob("*.png"))


def parse_image_size(thumb: Thumbnail):
    # pytest -s tests/test_thumbnail.py
    with Image.open(thumb.path) as img:
        print(f"{thumb.path.name} : {img.size}")
    with Image.open(thumb.output_file) as img:
        print(f"{thumb.output_file.name} : {img.size}", end="\n\n")


@pytest.mark.slow
class TestThumbnail:
    def test_thumbnail(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280))
            thumb.save_thumbnail()
            parse_image_size(thumb)

    def test_thumbnail_contain(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="contain")
            thumb.save_thumbnail()
            parse_image_size(thumb)

    def test_thumbnail_cover(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="cover")
            thumb.save_thumbnail()
            parse_image_size(thumb)

    def test_thumbnail_fit(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="fit")
            thumb.save_thumbnail()
            parse_image_size(thumb)

    def test_thumbnail_pad(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="pad")
            thumb.save_thumbnail()
            parse_image_size(thumb)

    def test_thumbnail_save_kwargs(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(
                img, out_dir, (400, 280), save_kwargs={"lossless": "True"}
            )
            thumb.save_thumbnail()
            parse_image_size(thumb)

    def test_thumbnail_operation_kwargs(self):
        print("=======================================")
        for img in images + png_files:
            thumb = Thumbnail(
                img,
                out_dir,
                (400, 280),
                operation="pad",
                operation_kwargs={"color": "white"},
            )
            thumb.save_thumbnail()
            parse_image_size(thumb)
