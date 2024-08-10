.. _multi_galleries:

==================
Multiple Galleries
==================

This page demonstrates how to create multiple galleries. There are two ways to create multiple galleries:

1. Provide a list of paths
2. Call the :func:`~myst_sphinx_gallery.gallery.generate_gallery` function multiple times

Provide a list of paths
-----------------------

You can provide a list of paths to the ``examples_dirs`` and ``gallery_dirs`` configuration option. This will create a gallery for each path in the list.

.. admonition:: conf.py

    The following configuration is used to in the ``conf.py`` file to create two galleries:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 5,6,10

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig, generate_gallery

        myst_sphinx_gallery_config = GalleryConfig(
            examples_dirs=["../../examples", "../../examples2"],
            gallery_dirs=["auto_examples", "auto_examples2"],
            root_dir=Path(__file__).parent,
            thumbnail_strategy="first",
        )
        generate_gallery(myst_sphinx_gallery_config)


Call the ``generate_gallery`` function multiple times
-----------------------------------------------------

You can call the :func:`~myst_sphinx_gallery.gallery.generate_gallery` function multiple times with different configurations to create multiple galleries.

.. admonition:: conf.py

    The following configuration is used to in the ``conf.py`` file for this gallery:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 5, 6, 11, 14, 15, 20

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

        myst_sphinx_gallery_config2 = GalleryConfig(
            examples_dirs="../../examples2",
            gallery_dirs="auto_examples2",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="markdown",
            thumbnail_strategy="first",
        )
        generate_gallery(myst_sphinx_gallery_config2)

.. tip::

    Since the :func:`~myst_sphinx_gallery.gallery.generate_gallery` function is called multiple times, you can provide different configurations for each gallery.
