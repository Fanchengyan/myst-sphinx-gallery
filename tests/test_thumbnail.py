from pathlib import Path

import pytest

from myst_sphinx_gallery.images import Thumbnail

cwd = Path(__file__).parent

data_dir = cwd / "data"
out_dir = cwd / "_build/thumbnails"

gif_files = list(data_dir.glob("*.gif"))

png_files = list(data_dir.glob("*.png"))


@pytest.mark.slow
class TestThumbnail:
    def test_thumbnail(self):
        print("=======================================")
        print("Test thumbnail")
        for img in gif_files + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280))
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_contain(self):
        print("=======================================")
        print("Test thumbnail contain")
        for img in gif_files + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="contain")
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_cover(self):
        print("=======================================")
        print("Test thumbnail cover")
        for img in gif_files + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="cover")
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_fit(self):
        print("=======================================")
        print("Test thumbnail fit")
        for img in gif_files + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), operation="fit")
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_pad(self):
        print("=======================================")
        print("Test thumbnail pad")
        for img in gif_files + png_files:
            thumb = Thumbnail(
                img,
                out_dir,
                operation="pad",
                operation_kwargs={"color": "white"},
                max_animation_frames=100,
                quality_animated=50,
            )
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_pad_1_frame_gif(self):
        print("=======================================")
        print("Test thumbnail pad")
        for img in gif_files:
            thumb = Thumbnail(
                img,
                out_dir,
                operation="pad",
                operation_kwargs={"color": "white"},
                max_animation_frames=1,
            )
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_save_kwargs(self):
        print("=======================================")
        print("Test thumbnail save kwargs")
        for img in gif_files + png_files:
            thumb = Thumbnail(img, out_dir, (400, 280), save_kwargs={"lossless": True})
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")

    def test_thumbnail_operation_kwargs(self):
        print("=======================================")
        print("Test thumbnail operation kwargs")
        for img in gif_files + png_files:
            thumb = Thumbnail(
                img,
                out_dir,
                (400, 280),
                operation="pad",
                operation_kwargs={"color": "white"},
            )
            thumb_file = thumb.save_thumbnail()
            print(img, thumb_file, sep=" -> ")
