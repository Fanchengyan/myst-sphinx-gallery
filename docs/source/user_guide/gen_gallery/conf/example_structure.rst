.. _structuring_examples:

=============================
Structuring files for Gallery
=============================

MyST Sphinx Gallery can help you to generate a gallery for a well-structured examples folder.

Basic rules
-----------

The file structure for the examples folder should follow the following rules:

1. A ``GALLERY_HEADER.rst`` file in the root folder of examples to display the gallery title and description.
2. Sub-folders with a ``GALLERY_HEADER.rst`` file in them to determine the sections in the gallery. This file contains title and description for the section.
3. Example files in the sub-folders. The example files can be jupyter notebooks (``.ipynb``), markdown (``.md``) or reStructuredText (``.rst``) files.



.. important::

    - The whole sub-folder will be ignored if it does not have the ``GALLERY_HEADER.rst`` file in it.
    - The ``GALLERY_HEADER.rst`` file will be converted to the ``index.rst`` for the gallery. Therefore, you need to use ``index`` rather that ``GALLERY_HEADER`` as the file name when cross-referencing.

Overview of the file structure
------------------------------

For example, if you have the following file structure in your Python project:

.. code-block:: bash
    :emphasize-lines: 12

    .
    ├── doc
    │   ├── conf.py
    │   ├── index.rst
    │   ├── user_guide.rst
    │   ├── api.rst
    |   ├── make.bat
    │   └── Makefile
    ├── python_module
    │   ├── __init__.py
    │   └── mod.py
    └── examples
        ├── GALLERY_HEADER.rst
        ├── 02-basic
        │    ├── GALLERY_HEADER.rst
        │    ├── 01-basic-example3.rst
        │    ├── 02-basic-example2.md
        │    └── 03-basic-example1.ipynb
        └── 01-advanced
            ├── GALLERY_HEADER.rst
            ├── 01-advanced-example3.rst
            ├── 02-advanced-example2.md
            └── 03-advanced-example1.ipynb


.. admonition:: conf.py
    :class: dropdown, note

    In this case, you can add the following configuration to the Sphinx ``conf.py`` file:

    .. code-block:: python
        :caption: conf.py

        myst_sphinx_gallery_config = GalleryConfig(
            examples_dirs="../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            ...
        )

The examples folder will be converted to the following gallery in the doc:

.. code-block:: bash
    :emphasize-lines: 3

    .
    └── doc
        ├── auto_examples(index)
        │    ├── advanced(index)
        │    │    ├── advanced-example3
        │    │    ├── advanced-example2
        │    │    └── advanced-example1
        │    └── basic(index)
        │         ├── basic-example3
        │         ├── basic-example2
        │         └── basic-example1
        ├── conf.py
        ├── index.rst
        ├── user_guide.rst
        ├── api.rst
        ├── make.bat
        └── Makefile

.. note::

    The number prefix in the directory/file names will be removed in the output gallery. See :ref:`example_order` for more details.

To refer to the gallery in the documentation, you can directly add the generated gallery index to the ``toctree`` directive in the ``index.rst`` file:

.. code-block:: rst
    :emphasize-lines: 6
    :caption: index.rst

    .. toctree::
        :maxdepth: 2
        :caption: Constants:

        user_guide
        auto_examples/index
        api
