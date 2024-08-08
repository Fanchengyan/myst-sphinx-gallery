from pathlib import Path

import pytest

from myst_sphinx_gallery.images import (
    CellImages,
    DocImages,
    parse_md_images,
    parse_rst_images,
)


@pytest.fixture
def nb_file():
    cwd = Path(__file__).parent
    nb_file = cwd.parent / "examples/code_markdown strategy/plot_image.ipynb"
    return nb_file


@pytest.fixture
def md_content():
    return """
    # Title

    ## Conventional markdown image syntax

    With alt text
    ![gallery_thumbnail](img/fun-fish.png)

    No alt text
    ![](img/fun-fish.png)

    ## MyST Images Syntax

    First alt text

    ```{image} img/fun-fish.png
        :alt: gallery_thumbnail
        :align: center
    ```

    Secondary alt text

    ```{image} img/fun-fish.png
        :align: center
        :alt: gallery_thumbnail
    ```

    No alt text

    ```{image} img/fun-fish.png
    ```

    ## MyST Figures Syntax

    First alt text

    ```{figure} img/fun-fish.png
        :alt: gallery_thumbnail
        :align: center
    ```

    Secondary alt text

    ```{figure} img/fun-fish.png
        :align: center
        :alt: gallery_thumbnail
    ```

    No alt text

    ```{figure} img/fun-fish.png
        :align: center
    ```
    """


@pytest.fixture
def rst_content():
    return """
    Title
    =====

    Image syntax
    ------------

    First alt text

    .. image:: img/fun-fish.png
        :alt: gallery_thumbnail
        :align: center
        
    Secondary alt text

    .. image:: img/fun-fish.png
        :align: center
        :alt: gallery_thumbnail
        
    No alt text

    .. image:: img/fun-fish.png
        :align: center
        
    Figure syntax
    -------------

    First alt text

    .. figure:: img/fun-fish.png
        :alt: gallery_thumbnail
        :align: center
        
    Secondary alt text

    .. figure:: img/fun-fish.png
        :align: center
        :alt: gallery_thumbnail
        
    No alt text

    .. figure:: img/fun-fish.png
        :align: center
"""


def test_parse_md_images(md_content):
    images = parse_md_images(md_content)
    assert images == DocImages(
        [
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", ""),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", ""),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", ""),
        ]
    )


def test_parse_rst_images(rst_content):
    images = parse_rst_images(rst_content)
    assert images == DocImages(
        [
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", ""),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", "gallery_thumbnail"),
            ("img/fun-fish.png", ""),
        ]
    )


def test_read_cell_image(nb_file):
    cell_img = CellImages(nb_file)
    assert len(cell_img) == 1
