.. _gallery3_header:

============================================
Examples-3 : Costumizing  Grid and Thumbnail
============================================


This is the **third gallery example**, which provides a comprehensive overview of
how to customize the grid layout, thumbnail behaviors for the gallery in the MyST Sphinx Gallery extension.


.. admonition:: conf.py
    :class: dropdown

    The following configuration is used to in the ``conf.py`` file for this gallery:

    .. code-block:: python
        :caption: conf.py
        :emphasize-lines: 9, 16, 26

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
        myst_gallery_grid.add_option("class-container", "myst-gallery-grid")

        myst_gallery_grid_item = GridItemCard(columns=4, margin=4, padding=4)
        myst_gallery_grid_item.add_option("class-item", "myst-gallery-grid-item")

        generate_gallery(
            GalleryConfig(
                examples_dirs="../../examples3",
                gallery_dirs="auto_examples3",
                root_dir=Path(__file__).parent,
                notebook_thumbnail_strategy="markdown",
                thumbnail_strategy="first",
                thumbnail_config=ThumbnailConfig(
                    ref_size=(320, 320),
                    operation="pad",
                    operation_kwargs={"color": "black"},
                    save_kwargs={"quality": 90},
                ),
                grid=myst_gallery_grid,
                grid_item_card=myst_gallery_grid_item,
            )
        )
