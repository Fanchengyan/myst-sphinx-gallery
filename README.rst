===================
MyST Sphinx Gallery
===================

MyST Sphinx Gallery is a Sphinx extension that builds a Sphinx Gallery from MyST Markdown/Notebook or RST files.

.. image:: docs/source/_static/gallery_example.png
    :align: center

Documentation
=============

The detailed documentation is available at: `<https://myst-sphinx-gallery.readthedocs.io/en/latest/>`_

Quick Start
===========

.. tip::
    The quick start guide in README is a brief introduction to the MyST Sphinx Gallery extension.
    The full documentation of ``Quick Start`` is available at: `Quick Start <https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/quick_start.html>`_.

Installation
------------

**MyST Sphinx Gallery** is a Python package, and requires ``Python >= 3.8``. You can install the latest release using ``pip`` from the PyPI:

.. code-block:: bash

    pip install myst_sphinx_gallery



Configure and usages
--------------------

To use MyST Sphinx Gallery, you need to add the following code to the Sphinx ``conf.py`` file:

.. code-block:: python

    from pathlib import Path

    from myst_sphinx_gallery import GalleryConfig, generate_gallery

    myst_sphinx_gallery_config = GalleryConfig(
        examples_dirs="../../examples",
        gallery_dirs="auto_examples",
        root_dir=Path(__file__).parent,
        notebook_thumbnail_strategy="code",
    )
    generate_gallery(myst_sphinx_gallery_config)

.. tip::

    You can **generate multiple galleries** by proper configuration in the ``conf.py`` file. For more details, please refer to the `Multiple Galleries <https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/multi_galleries.html>`_.


Construct the examples folder
-----------------------------

To generate the gallery, you need to create a well-structured examples folder. The detailed documentation of structuring files for gallery is available at: `Structuring files for Gallery <https://myst-sphinx-gallery.readthedocs.io/en/latest/user_guide/example_structure.html>`_.
