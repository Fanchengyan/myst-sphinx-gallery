<h1 align="center">
<img src="https://raw.githubusercontent.com/Fanchengyan/myst-sphinx-gallery/main/docs/source/_static/logo/logo.svg" width="400">
</h1><br>


[![Conda Recipe](https://img.shields.io/badge/recipe-myst--sphinx--gallery-green.svg)](https://anaconda.org/conda-forge/myst-sphinx-gallery)
[![Documentation Status](https://readthedocs.org/projects/myst-sphinx-gallery/badge/?version=latest)](https://myst-sphinx-gallery.readthedocs.io/en/latest/?badge=latest)
[![Language](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat-square)](https://www.python.org/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/myst-sphinx-gallery.svg)](https://anaconda.org/conda-forge/myst-sphinx-gallery)
[![PyPI](https://img.shields.io/pypi/v/myst-sphinx-gallery)](https://pypi.org/project/myst-sphinx-gallery/)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/myst-sphinx-gallery.svg)](https://anaconda.org/conda-forge/myst-sphinx-gallery)
[![tests](https://github.com/Fanchengyan/myst-sphinx-gallery/actions/workflows/tests.yml/badge.svg)](https://github.com/Fanchengyan/myst-sphinx-gallery/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/Fanchengyan/myst-sphinx-gallery/graph/badge.svg?token=IHXYE1K1G9)](https://codecov.io/gh/Fanchengyan/myst-sphinx-gallery)


## Introduction

**MyST Sphinx Gallery** is a Sphinx extension that allows you to build
galleries from jupyter notebooks (`.ipynb`), markdown (`.md`) or
reStructuredText (`.rst`) files.

This extension is functionally similar to the
[Sphinx-Gallery](https://sphinx-gallery.github.io/stable/index.html)
extension, but aim to provide a simple and efficient way to create
galleries written in a variety of file formats.


![gallery_example](docs/source/_static/gallery_example.png)

## Highlight Features

- **Easy to use** - It provides a set of `directives` to generate
  galleries, as simple as adding `toctree`.
- **Flexible** - You can easily generate a gallery of examples from your
  Jupyter Notebooks, Markdown, or reStructuredText files. It works with `MyST` Ecosystem, including [MyST-parser](https://myst-parser.readthedocs.io/en/latest/) and [MyST-NB](https://myst-nb.readthedocs.io/en/latest/), to render markdown or jupyter notebooks in Sphinx documentation.
- **Fast and robust** - It utilizes existing images to generate gallery
  thumbnails, eliminating code execution delays and potential accidental errors
  when building gallery.
- **Customizable** - You can customize the gallery, such as thumbnail
  selection, and style of the gallery.


## Documentation

The detailed documentation is available at: [https://myst-sphinx-gallery.readthedocs.io/en/latest/](https://myst-sphinx-gallery.readthedocs.io/en/latest/)

## Quick Start

> [!NOTE]
> The quick start guide here is a brief introduction to the MyST Sphinx Gallery extension. More detailed Quick Start guide is available at: [Quick Start](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/quick_start.html).


## Installation

**MyST Sphinx Gallery** is a Python package, and requires `Python >= 3.8`. You can install the latest release using `pip` from the PyPI:

```bash
pip install myst_sphinx_gallery
```

or using `conda` / `mamba` from the conda-forge channel:

```bash
conda install -c conda-forge myst-sphinx-gallery
```

```bash
mamba install -c conda-forge myst-sphinx-gallery
```

## Configuring the extension

### Enable the extension

After installation, you can enable the extension in Sphinx `conf.py` file:

```python
  extensions = [
      ...,  # other extensions
      "myst_sphinx_gallery",
  ]
```

>[!IMPORTANT]
>**MyST Sphinx Gallery only helps you to generate the gallery**. You need to enable the MyST parsers to render the markdown or jupyter notebook files by yourself.
>
>For instance, to enable the MyST-NB, you can add the following code to the `conf.py` file:
>
>```python
>extensions = [
>    ...,
>    "myst_nb",
>]
>
>source_suffix = {
>    ".rst": "restructuredtext",
>    ".md": "myst-nb",
>    ".myst": "myst-nb",
>}
>```
>
>For more information, please refer to the documentation of [MyST](https://myst-parser.readthedocs.io/en/latest/) and [MyST-NB](  https://myst-nb.readthedocs.io/en/latest/).

## Configuring the variables


MyST Sphinx Gallery has two main configuration variables that can be set in
your `conf.py` file.

- `myst_sphinx_gallery_config` : **global configuration** for all examples
  using gallery directives or used to **generate galleries**.
- `myst_sphinx_gallery_files_config` : **configuration for individual files**
  to override the global configuration for those files.

> [!TIP]
>Those two variables are optional and can be omitted if you don't need to  customize the behavior of MyST-Sphinx-Gallery.

More details about the configuration variables can be found in the
[Configuration Variables](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/config.html) section.

## Generating gallery

There are two ways to generate galleries in MyST Sphinx Gallery:

1. **Using directives:** MyST Sphinx Gallery provides three directives for generating galleries: `base-gallery`, `gallery`, and `ref-gallery`. You can directly use these directives to generate galleries in reStructuredText (`.rst`), Markdown (`.md`), and Jupyter Notebook (`.ipynb`) files.
2. **Configuring in conf.py:** You can also generate gallery by specifying the examples and gallery directories in your `conf.py` file. This method is keeping in line with [Sphinx Gallery](https://sphinx-gallery.github.io/stable/index.html) extension.


> [!NOTE]
>**Using directives** is highly recommended for generating galleries as it provides more options and flexibility. For instance, you can add `tooltip` to example cards, **call different directives multi-times in a single file** to generate a complex gallery. This cannot be done using the configuration method.

You can refer to the [Generating Galleries Methods](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/gen_gallery.html) section for more details.



## Select the thumbnail for an example file

- **one image** - If there only one image in an example file, no additional configuration is needed, and that image will be used as the gallery thumbnail.
- **multiple images** - If there are multiple figures in an example file, you can specify the strategy to determine which thumbnail will be used for the gallery. The following strategies are supported:
  1. **alt** - If the alt attribute of an image/figure is set to gallery_thumbnail, that image/figure will be used as the gallery thumbnail for this file.
  2. **first/last** - If there are multiple images that can be used as the gallery thumbnail, the first/last image will be selected. You can specify the strategy by setting the thumbnail_strategy in the configuration file. The default value is first.
  3. **code/markdown** - For Jupyter notebook files, both markdown and code cells can contain images. You can specify the strategy by setting the notebook_thumbnail_strategy in the configuration file. The default value is code.
- **no image** - If no image/figure is found, the default thumbnail will be used.


More details can be found in the [Thumbnail Strategies](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/thumb.html).

## Customizing style of thumbnail and card

You can customize the layout and thumbnail behaviors for the gallery using the MyST Sphinx Gallery extension. For more details, please refer to the section [Customizing Style of Thumbnail and Card
](https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/custom.html).
