# MyST Sphinx Gallery

MyST Sphinx Gallery is a Sphinx extension that builds a Sphinx Gallery from MyST Markdown/Notebook or RST files.

![gallery_example](docs/source/_static/gallery_example.png)

## Documentation

The detailed documentation is available at: [https://myst-sphinx-gallery.readthedocs.io/en/latest/](https://myst-sphinx-gallery.readthedocs.io/en/latest/)

## Quick Start

> [!NOTE] The quick start guide in README is a brief introduction to the MyST Sphinx Gallery extension. The full documentation of "Quick Start" is available at: [Quick Start](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/quick_start.html).

## Installation

**MyST Sphinx Gallery** is a Python package, and requires `Python >= 3.8`. You can install the latest release using `pip` from the PyPI:

```bash
pip install myst_sphinx_gallery
```

## Configure and usages

To use MyST Sphinx Gallery, you need to add the following code to the Sphinx `conf.py` file:

```python
from pathlib import Path

from myst_sphinx_gallery import GalleryConfig, generate_gallery

generate_gallery(GalleryConfig(
    examples_dirs="../../examples",
    gallery_dirs="auto_examples",
    root_dir=Path(__file__).parent,
    notebook_thumbnail_strategy="code",
))
```

> [!NOTE] You can **generate multiple galleries** by proper configuration in the `conf.py` file. For more details, please refer to the [Multiple Galleries](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/multi_galleries.html).

## Construct the examples folder

To generate the gallery, you need to create a well-structured examples folder. The detailed documentation of structuring files for gallery is available at: [Structuring files for Gallery](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/example_structure.html).
