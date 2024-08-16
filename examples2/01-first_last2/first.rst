==================
``first`` strategy
==================

This is a gallery example with image URLs in the ``.rst`` file to test ``first`` strategy. Since no ``alt`` attribute is set to ``gallery_thumbnail``, the last image in the file will be used as the thumbnail for the gallery.

.. admonition:: conf.py
    :class: dropdown

    The following configuration is used to set the strategy to ``first``:

    .. code-block:: python
        :caption: conf.py

        myst_sphinx_gallery_config = GalleryConfig(
            ...,
            thumbnail_strategy = "first",
            )

    See :ref:`code_markdown` for more details.

.. code-block:: rst

    .. image:: /_static/barchart.png
        :align: center

.. image:: /_static/barchart.png
    :align: center
    :width: 60%

.. code-block:: rst

    .. image:: /_static/bar_colors.png
        :align: center
        :width: 60%

.. image:: /_static/bar_colors.png
    :align: center
    :width: 60%

.. code-block:: rst

    .. figure:: /_static/stackplot_demo.png
        :align: center

        This is a caption.

.. figure:: /_static/stackplot_demo.png
    :align: center
    :width: 60%

    This is a caption.
