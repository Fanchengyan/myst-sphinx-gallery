.. _configuration:

======================================
Configuration for Generating Galleries
======================================


This page describes how to

- setup configuration for the gallery using the ``myst_sphinx_gallery`` extension
- create **multiple galleries** or **sub-galleries**


Setup for Galleries in ``conf.py``
==================================

There are two ways to setup configuration for the gallery in the :file:`conf.py` file:

1. add the ``myst_sphinx_gallery`` extension to the ``extensions`` list and specify the ``myst_sphinx_gallery_config`` variable.
2. directly call the :func:`~myst_sphinx_gallery.generate_gallery` function directly in the ``conf.py`` file.


Add extension to the ``extensions`` list
----------------------------------------

You can add the ``myst_sphinx_gallery`` extension to the ``extensions`` list and specify the ``myst_sphinx_gallery_config`` variable in the ``conf.py`` file to configure the gallery.

.. note::

    You can only generate galleries with the same configuration in this manner.
    If you want to create **multiple galleries with different configurations**
    or **sub-galleries**, please refer to :ref:`call_function_directly` and :ref:`multi_galleries`.


.. admonition:: Example conf.py

    The following configuration is an example of how to configure the gallery in the ``conf.py`` file in this manner:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 1, 9

        extensions = [
            ...,  # other extensions
            "myst_sphinx_gallery",
        ]

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig

        myst_sphinx_gallery_config = GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
            thumbnail_strategy="last",
        )


The parameters in the ``myst_sphinx_gallery_config`` variable will be used to configure the gallery. Available parameters can be found in the :class:`~myst_sphinx_gallery.GalleryConfig` class.

.. tip::

    - The ``myst_sphinx_gallery_config`` variable can either be a instance of :class:`~myst_sphinx_gallery.GalleryConfig` class or a dictionary with the same keys as the :class:`~myst_sphinx_gallery.GalleryConfig` class.
    - The :class:`~myst_sphinx_gallery.GalleryConfig` is recommended as it provides type hints, which can be helpful for IDEs and linters.


.. _call_function_directly:

Call the function directly
--------------------------

Call ``generate_gallery`` function for galleries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :func:`~myst_sphinx_gallery.generate_gallery` function can be called
directly in the ``conf.py`` file to generate the galleries.


.. admonition:: Example conf.py

    The following configuration is an example of how to configure the gallery in the ``conf.py`` file in this manner:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 4

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig, generate_gallery

        generate_gallery(
            GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
            thumbnail_strategy="last",
            )
        )

.. hint::

    In this case, there is no need to adding the ``myst_sphinx_gallery`` extension in the ``extensions`` list or specifying the ``myst_sphinx_gallery_config`` variable.


.. _multi_galleries:

Configure multiple galleries
============================

There are two ways to create multiple galleries:

1. Provide a list of paths
2. Call the :func:`~myst_sphinx_gallery.generate_gallery` function multiple times

Provide a list of paths
-----------------------

You can provide a list of paths to the ``examples_dirs`` and ``gallery_dirs`` configuration option. This will create a gallery for each path in the list.

.. admonition:: Example conf.py

    The following configuration is used to in the ``conf.py`` file to create two galleries:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 6, 7

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig, generate_gallery

        generate_gallery(
            GalleryConfig(
            examples_dirs=["../../examples", "../../examples2"],
            gallery_dirs=["auto_examples", "auto_examples2"],
            root_dir=Path(__file__).parent,
            )
        )


Call the ``generate_gallery`` function multiple times
-----------------------------------------------------

You can call the :func:`~myst_sphinx_gallery.generate_gallery` function multiple times with different configurations to create multiple galleries.

.. admonition:: Example conf.py

    The following configuration is an example of how to configure multiple galleries in the ``conf.py`` file in this manner:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 5, 16

        from pathlib import Path
        from myst_sphinx_gallery import GalleryConfig, generate_gallery

        # generate first gallery
        generate_gallery(
            GalleryConfig(
            examples_dirs="../../examples",
            gallery_dirs="auto_examples",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="code",
            thumbnail_strategy="last",
            )
        )

        # generate second gallery
        generate_gallery(
            GalleryConfig(
            examples_dirs="../../examples2",
            gallery_dirs="auto_examples2",
            root_dir=Path(__file__).parent,
            notebook_thumbnail_strategy="markdown",
            thumbnail_strategy="first",
            )
        )

.. tip::

    Since the :func:`~myst_sphinx_gallery.generate_gallery` function is called multiple times, you can provide different configurations for each gallery.
