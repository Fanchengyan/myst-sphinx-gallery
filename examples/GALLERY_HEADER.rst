.. _gallery_header:

===============
Gallery Example
===============

This is the **first gallery example**, which provides a comprehensive overview of the MyST Sphinx Gallery extension.

Additional illustrations of the thumbnail strategies can be found in :ref:`gallery2_header`.


.. admonition:: conf.py
    :class: dropdown

    The following configuration is used to in the ``conf.py`` file for this gallery:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 8,9

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig, generate_gallery

        myst_sphinx_gallery_config = GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
            thumbnail_strategy="last",
        )
        generate_gallery(myst_sphinx_gallery_config)
