.. _cross_reference:

======================================
Cross-reference to Examples in Gallery
======================================

When you generate the gallery, each example file will be automatically added
a target for cross-referencing. This feature allows you to refer to those
example files in the other documentation files.

Rule for generating targets
---------------------------

For example files
~~~~~~~~~~~~~~~~~

- removing the number prefix ``dd-`` (if exists) and file suffix.
- converring the letters in the file name to lowercase (target must be small letters).
- adding the prefix to the file name. (default is ``example_``)

.. note::

    The target is generated based on the file name, so you need to make sure the file name is unique.


For ``GALLERY_HEADER.rst`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The rules are the same as the example files, except:

- target is generated based on the folder name.
- adding a suffix ``_header`` to avoid conflict with the example files.
  (need version 0.2.2 or later)

.. versionchanged:: 0.2.1

    Before version 0.2.1, you need to add the target manually in the
    ``GALLERY_HEADER.rst`` file.



Example of target generation
----------------------------

For example, the file ``examples/basic/01-Basic-Example1.ipynb`` will be added
a target named ``example_basic-example1`` in the first line/(markdown cell) of
the file.

You can refer to this target in the documentation using the following syntax:

in a ReStructuredText file (``*.rst``)

.. code-block:: rst

    :ref:`example_basic-example1`

in a Markdown/Notebook file ( ``*.md``/ ``*.ipynb`` ) with MyST syntax

.. code-block:: markdown

    [Basic Usages](#example_basic-example1)


Customizing the target prefix
-----------------------------

.. versionadded:: 0.2.1

You can customize the target prefix by setting the ``target_prefix`` parameter in the :class:`~myst_sphinx_gallery.GalleryConfig` class in the ``conf.py`` file.

For example, you can change the target prefix to ``myst_gallery_`` by adding the following code in the ``conf.py`` file:

.. code-block:: python
    :caption: conf.py
    :emphasize-lines: 8

    from myst_sphinx_gallery import generate_gallery, GalleryConfig

    generate_gallery(
        GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            target_prefix="myst_gallery_",
            ...
        )
    )
