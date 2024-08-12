.. _gallery_header:

======================================
Examples 1 : Select thumbnail strategy
======================================

This is the **first gallery example**, which provides a comprehensive overview of
how to select a thumbnail for one example file in the MyST Sphinx Gallery extension.

Additional illustrations of the strategies of selecting thumbnail can be found in :ref:`gallery2_header`.


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
            examples_dirs="../../examples1",
            gallery_dirs="auto_examples1",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
            thumbnail_strategy="last",
            )
        )
