
.. _custom:

================================
Customizing Layout and Thumbnail
================================

This page demonstrates how to customize the grid layout and thumbnail behaviors
for the gallery using the MyST Sphinx Gallery extension.

.. tip::

    The :ref:`gallery3_header` is an example gallery used to demonstrate the
    customization of the layout and thumbnail using the MyST Sphinx Gallery
    extension, providing an intuitive understanding of customizing behaviors.

Customizing thumbnail
---------------------

By default, the thumbnail is resized to (320, 224) pixels with a ``pad``
operation and a white background color. You can customize the thumbnail
behavior by providing a different configuration to the
:class:`~myst_sphinx_gallery.ThumbnailConfig` class.

For example, you can change the thumbnail size to (320, 320) pixels with a
``pad`` operation and a orange background color by adding the following code in
the ``conf.py`` file:

.. code-block:: python
    :caption: conf.py

    from myst_sphinx_gallery import generate_gallery, GalleryConfig, ThumbnailConfig

    generate_gallery(
        GalleryConfig(
            examples_dirs="../../examples3",
            gallery_dirs="auto_examples3",
            root_dir=Path(__file__).parent,
            thumbnail_config=ThumbnailConfig(
                ref_size=(320, 320),
                operation="pad",
                operation_kwargs={"color": "orange"},
                quality_static=90,
            ),
            ..., # other configurations
        )
    )

Customizing layout
------------------

Customizing grid
~~~~~~~~~~~~~~~~

The `sphinx-design <https://sphinx-design.readthedocs.io/en/latest/grids.html>`_
package is used to create the grid layout of the gallery. MyST Sphinx Gallery
provides two classes, :class:`~myst_sphinx_gallery.Grid` and
:class:`~myst_sphinx_gallery.GridItemCard`, to customize the layout of the
gallery.

For example, you can change the grid option to ``(1,2,2,2)``, which means the
colums of the gallery will be 2 colums for the wide screen and 1 column for the
small screen. You can also change the padding or margin of the grid and grid
cards by specifying the ``padding`` and ``margin`` parameters in the
:class:`~myst_sphinx_gallery.Grid` and :class:`~myst_sphinx_gallery.GridItemCard`
classes.

Following code is an example of customizing the layout of the gallery:

.. code-block:: python
    :caption: conf.py

    from myst_sphinx_gallery import generate_gallery, GalleryConfig, Grid, GridItemCard

    generate_gallery(
        GalleryConfig(
            examples_dirs="../../examples3",
            gallery_dirs="auto_examples3",
            root_dir=Path(__file__).parent,
            grid=Grid(
                grid_option=(1, 2, 2, 2),
                margin=3,
                padding=2,
            ),
            grid_item_card=GridItemCard(columns=5, margin=3, padding=3),
            ..., # other configurations
        )
    )


Customizing by CSS
~~~~~~~~~~~~~~~~~~

The :class:`~myst_sphinx_gallery.Grid` and
:class:`~myst_sphinx_gallery.GridItemCard` classes provide a ``add_option()``
method, which can be used to add custom CSS classes to the grid and grid cards.

For example, you can add a custom class to the grid and grid cards by adding the
following code in the ``conf.py`` file:


.. code-block:: python
    :caption: conf.py
    :emphasize-lines: 8, 11

    from myst_sphinx_gallery import generate_gallery, GalleryConfig, Grid, GridItemCard

    myst_gallery_grid = Grid(
        grid_option=(1, 2, 2, 2),
        margin=3,
        padding=2,
    )
    myst_gallery_grid.add_option("class-container", "myst-gallery-grid")

    myst_gallery_grid_item = GridItemCard(columns=5, margin=3, padding=3)
    myst_gallery_grid_item.add_option("class-item", "myst-gallery-grid-item")

    generate_gallery(
        GalleryConfig(
            examples_dirs="../../examples3",
            gallery_dirs="auto_examples3",
            root_dir=Path(__file__).parent,
            grid=myst_gallery_grid,
            grid_item_card=myst_gallery_grid_item,
        )
    )


Then, you can control the style of the grid and grid cards by specifying the
custom parameters in the ``_static/css/gallery.css`` file.

.. tip::

    To enable the custom CSS file, you need to add the following code in the ``conf.py`` file:

    .. code-block:: python
        :caption: conf.py


        html_static_path = ["_static"]

        html_css_files = [
            ..., # other CSS files
            "css/gallery.css",
        ]


Following code is an example of customizing the style of the grid and grid cards:

.. code-block:: css
    :caption: _static/css/gallery.css

    /* custom style for grid */
    .myst-gallery-grid {
        /* custom parameters */
    }

    /* custom style for grid items */
    .myst-gallery-grid-item .sd-card-img-top {
        margin: 10px auto;
        background: none !important;
        width: 80%;
        display: block;
    }
    .myst-gallery-grid-item .sd-card-body {
        margin: 1px auto;
        display: block;
    }

    .myst-gallery-grid-item .sd-card-title .reference {
        color: var(--pst-color-warning);
        font-size: var(--pst-font-size-h5);
        font-weight: lighter;
    }
