.. _customizing_grid_and_thumbnail:

==============================================
Examples-3 : Customizing  Layout and Thumbnail
==============================================

This is the **third gallery example**, which provides an intuitive understanding of
the grid layout and thumbnail behaviors when customizing the gallery using the MyST Sphinx Gallery extension.


.. hint::
    The following configurations are used in this gallery example:

    - **Thumbnail**: The thumbnail is generated using the ``pad`` operation with a **orange** background color and a quality of 90. The figures are resized to a reference size of (320, 320).
    - **Grid Layout**: The grid layout is customized using the :class:`myst_sphinx_gallery.Grid` and
      :class:`myst_sphinx_gallery.GridItemCard` classes with different margin and padding values.
    - **CSS**: The CSS is used to customize the thumbnail and card layout in the gallery. The thumbnail is centered with a margin of 10px, and the card title is centered and colored with a **orange** (warning) color.


    .. admonition:: conf.py
        :class: dropdown

        The following configuration is used to in the ``conf.py`` file for this gallery:

        .. code-block:: python
            :caption: conf.py
            :emphasize-lines: 9, 15, 25

            from myst_sphinx_gallery import (
                GalleryConfig,
                Grid,
                GridItemCard,
                ThumbnailConfig,
                generate_gallery,
            )

            myst_gallery_grid = Grid(
                grid_option=(1,2,2,2),
                margin=3,
                padding=2,
            )

            myst_gallery_grid_item = GridItemCard(columns=4, margin=4, padding=4)
            myst_gallery_grid_item.add_option("class-item", "myst-gallery-grid-item")

            generate_gallery(
                GalleryConfig(
                    examples_dirs="../../examples3",
                    gallery_dirs="auto_examples3",
                    root_dir=Path(__file__).parent,
                    notebook_thumbnail_strategy="markdown",
                    thumbnail_strategy="last",
                    thumbnail_config=ThumbnailConfig(
                        ref_size=(320, 320),
                        operation="pad",
                        operation_kwargs={"color": "orange"},
                        quality_static=90,
                    ),
                    grid=myst_gallery_grid,
                    grid_item_card=myst_gallery_grid_item,
                )
            )

    .. admonition:: gallery.css
        :class: dropdown

        The following CSS is used to in the ``gallery.css`` file for this gallery:

        .. code-block:: css

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

            .myst-gallery-grid-item .sd-card-hover {
                border: 1px solid var(--pst-color-warning);
            }

            .myst-gallery-grid-item .sd-card-title .reference {
                color: var(--pst-color-warning);
                font-size: var(--pst-font-size-h5);
                font-weight: lighter;
            }

        .. tip::

            - The ``.myst-gallery-grid-item`` in the CSS is defined in the ``myst_gallery_grid_item.add_option("class-item", "myst-gallery-grid-item")`` in the ``conf.py`` file.
            - You can give a different class name to the grid item card and use it in the CSS file if this class name is not suitable for your project.
