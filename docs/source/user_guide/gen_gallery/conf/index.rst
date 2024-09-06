.. _config_in_conf:

==========================
Configuring in ``conf.py``
==========================

Configuration and usages
------------------------

To use MyST Sphinx Gallery, you can add the following code to the Sphinx
``conf.py`` file:

.. code-block:: python
    :caption: conf.py

    from pathlib import Path

    from myst_sphinx_gallery import GalleryConfig, generate_gallery

    myst_sphinx_gallery_config = GalleryConfig(
        examples_dirs="../../examples",
        gallery_dirs="auto_examples",
        root_dir=Path(__file__).parent,
        notebook_thumbnail_strategy="code",
    )


All configuration can be done by specifying the parameters to the
:class:`GalleryConfig <myst_sphinx_gallery.config.GalleryConfig>`.

.. tip::

    You can generate **multiple galleries** by proper configuration in the ``conf.py`` file. For more details, please refer to the :ref:`multi_galleries`.


Construct the examples folder
-----------------------------

To generate the gallery, you need to create a well-structured examples folder.
The examples folder should contain the following files/directories:

1. A ``GALLERY_HEADER.rst`` file in the root folder of examples to display
   the gallery title and description.
2. Sub-folders with a ``GALLERY_HEADER.rst`` file in them to determine the
   sections in the gallery. This file contains title and description for
   the section.
3. Example files in the sub-folders. The example files can be jupyter
   notebooks (``.ipynb``), markdown (``.md``) or reStructuredText (``.rst``)
   files.

For more details, please refer to the :ref:`structuring_examples`.


Define the order of the examples
--------------------------------

MyST Sphinx Gallery using files/directories order to determine the order of
the gallery. To specify the order of the files/directories, you can add a
number ``dd-`` prefix at the beginning of the file name. The number will be
automatically removed from the file name in the output gallery.


More details can be found in the :ref:`example_order`.


.. toctree::
    :hidden:

    setup_galleries
    example_structure
    order
    cross_reference
