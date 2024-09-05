.. _demo_gallery:

============
Demo Gallery
============

This gallery demonstrates the functionality of the
**MyST Sphinx Gallery** extension.

Thumbnail selection strategies
==============================

This section provides a comprehensive overview
of how to select a thumbnail for one example file in the
**MyST Sphinx Gallery** extension.

.. admonition:: Code for this gallery
    :class: dropdown

    The code for this gallery is:

    .. code-block:: rst
        :caption: index.rst

        .. gallery::
            :tooltip:
            :caption: Thumbnail selection strategies

            alt/index
            first_last/index
            code_markdown/index
            default/index

    Following is the code used to customize the thumbnail selection strategies
    for each example file in the ``conf.py``:

    .. code-block:: python
        :caption: conf.py

        from myst_sphinx_gallery import FilesConfig, GalleryThumbnailConfig

        myst_sphinx_gallery_files_config = FilesConfig(
            named_config={
                "first_md": GalleryThumbnailConfig(
                    thumbnail_strategy="first", notebook_thumbnail_strategy="markdown"
                ),
                "first_code": GalleryThumbnailConfig(
                    thumbnail_strategy="first", notebook_thumbnail_strategy="code"
                ),
                "last_md": GalleryThumbnailConfig(
                    thumbnail_strategy="last", notebook_thumbnail_strategy="markdown"
                ),
                "last_code": GalleryThumbnailConfig(
                    thumbnail_strategy="last", notebook_thumbnail_strategy="code"
                ),

            },
            files_config={
                "first_code": [
                    "examples/code_markdown/first code.ipynb",
                    ],
                "last_code": [
                    "examples/code_markdown/last code.ipynb",
                    ],
                "first_md": [
                    "examples/code_markdown/first markdown.ipynb",
                    "examples/first_last/first.rst",
                    ],
                "last_md": [
                    "examples/code_markdown/last markdown.ipynb",
                    "examples/first_last/last.rst",
                    ],
            },
        )

.. gallery::
    :tooltip:
    :caption: Thumbnail selection strategies

    alt/index
    first_last/index
    code_markdown/index
    default/index

Ref Gallery
===========

This section provides a demo of a gallery with references
to the examples.

.. admonition:: Code for this gallery
    :class: dropdown

    The code for this gallery is:

    .. code-block:: rst
        :caption: index.rst


        .. base-gallery::
            :tooltip:
            :caption: Ref Gallery

            ref_gallery/code_ref
            ref_gallery/rst_ref

.. base-gallery::
    :tooltip:
    :caption: Ref Gallery

    ref_gallery/code_ref
    ref_gallery/rst_ref


No tooltip
==========

This section provides a demo of a gallery with no tooltips.
When you hover over the example cards, no tooltips will appear.

.. admonition:: Code for this gallery
    :class: dropdown

    The code for this gallery is:

    .. code-block:: rst
        :caption: index.rst
        :emphasize-lines: 2

        .. ref-gallery::

            examples/alt/rst image
            examples/first_last/first
            examples/code_markdown/first code

.. ref-gallery::

    examples/alt/rst image
    examples/first_last/first
    examples/code_markdown/first code
