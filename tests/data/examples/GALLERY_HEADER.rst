.. _gallery2_header:

======================================
Examples-2 : Select thumbnail strategy
======================================

This is the **second gallery example**. It is used to

- illustrate **multiple galleries**.
- provide **additional illustrations** of the strategies of selecting thumbnail.

the more comprehensive examples can be found in :ref:`gallery_header`.

.. admonition:: conf.py
    :class: dropdown

    The following configuration is used to in the ``conf.py`` file for this gallery:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 9, 10

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig, generate_gallery

        generate_gallery(
            GalleryConfig(
            examples_dirs="../../examples2",
            gallery_dirs="auto_examples2",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="markdown",
            thumbnail_strategy="first",
            )
        )
