.. _quick_start:

===========
Quick Start
===========

This page gives a quick start guide of how to get started with MyST Sphinx Gallery.

Installation
------------

**MyST Sphinx Gallery** is a Python package, and requires ``Python >= 3.8``.
You can install the latest release using ``pip`` or ``conda`` / ``mamba``:

.. tab-set::

    .. tab-item:: pip

        .. code-block:: bash

            pip install myst-sphinx-gallery

    .. tab-item:: conda

        .. code-block:: bash

            conda install -c conda-forge myst-sphinx-gallery

    .. tab-item:: mamba

        .. code-block:: bash

            mamba install -c conda-forge myst-sphinx-gallery


Configure and usages
--------------------

To use MyST Sphinx Gallery, you need to add the following code to the Sphinx
``conf.py`` file:

.. code-block:: python
    :caption: conf.py

    from pathlib import Path

    from myst_sphinx_gallery import GalleryConfig, generate_gallery

    generate_gallery(
        GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
        )
    )

You can configure all options by specifying the parameters for
:class:`GalleryConfig <myst_sphinx_gallery.config.GalleryConfig>`.

.. tip::

    You can generate **multiple galleries** by proper configuration in the ``conf.py`` file. For more details, please refer to the :ref:`multi_galleries`.


.. important::

    **MyST Sphinx Gallery only helps you to generate the gallery**. You need to enable the MyST parsers to render the markdown or jupyter notebook files by yourself.

    For instance, to enable the MyST-NB, you can add the following code to the ``conf.py`` file:

    .. code-block:: python
        :caption: conf.py

        extensions = [
            ...,
            "myst_nb",
        ]

        source_suffix = {
            ".rst": "restructuredtext",
            ".md": "myst-nb",
            ".myst": "myst-nb",
        }

    For more information, please refer to the documentation of `MyST <https://myst-parser.readthedocs.io/en/latest/>`_ and `MyST-NB  <https://myst-nb.readthedocs.io/en/latest/>`_.

Construct the examples folder
-----------------------------

To generate the gallery, you need to create a well-structured examples folder.
The examples folder should contain the following files/directories:

1. A ``GALLERY_HEADER.rst`` file in the root folder of examples to display the gallery title and description.
2. Sub-folders with a ``GALLERY_HEADER.rst`` file in them to determine the sections in the gallery. This file contains title and description for the section.
3. Example files in the sub-folders. The example files can be jupyter notebooks (``.ipynb``), markdown (``.md``) or reStructuredText (``.rst``) files.

For more details, please refer to the :ref:`structuring_examples`.


Define the order of the examples
--------------------------------

MyST Sphinx Gallery using files/directories order to determine the order of
the gallery. To specify the order of the files/directories, you can add a
number ``dd-`` prefix at the beginning of the file name. The number will be
automatically removed from the file name in the output gallery.


More details can be found in the :ref:`example_order`.

Select the thumbnail for an example file
----------------------------------------

- **one image** - If there only one image in an example file, no additional configuration is needed, and that image will be used as the gallery thumbnail.

- **multiple images** - If there are multiple figures in an example file, you can specify the strategy to determine which thumbnail will be used for the gallery. The following strategies are supported:

  1. **alt** - If the alt attribute of an image/figure is set to ``gallery_thumbnail``, that image/figure will be used as the gallery thumbnail for this file.
  2. **first/last** - If there are multiple images that can be used as the gallery thumbnail, the first/last image will be selected. You can specify the strategy by setting the ``thumbnail_strategy`` in the configuration file. The default value is ``first``.
  3. **code/markdown** - For Jupyter notebook files, both markdown and code cells can contain images. You can specify the strategy by setting the ``notebook_thumbnail_strategy`` in the configuration file. The default value is ``code``.

- **no image** - If no image/figure is found, the default thumbnail will be used.

More details can be found in the :ref:`thumbnail_strategy`.

Customize the layout and thumbnail
----------------------------------

You can customize the layout and thumbnail behaviors for the gallery using
the MyST Sphinx Gallery extension. For more details, please refer to the
section :ref:`custom`.

.. tip::

    The :ref:`gallery3_header` is an example gallery used to demonstrate the customization of the layout and thumbnail, providing an intuitive understanding of customizing behaviors.
