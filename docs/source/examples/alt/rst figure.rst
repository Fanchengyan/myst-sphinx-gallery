====================
Rst Figure Directive
====================

This is a ``.rst`` file with ``figure`` directive.
The example thumbnail is selected with ``figure`` directive ``alt`` option
being set to ``gallery_thumbnail``.


figure directive without ``alt`` text
-------------------------------------

This ``figure`` directive does not have any ``alt`` text. Therefore, will not
be used as the thumbnail for the gallery.

.. code-block:: rst

    .. figure:: /_static/barchart.png
        :align: center

    This is a caption.

.. figure:: /_static/barchart.png
    :align: center

    This is a caption.


figure directive with ``alt`` text
----------------------------------

This figure directive has set the ``alt`` attribute to ``gallery_thumbnail``.
Therefore, This figure will be used as the thumbnail for the gallery.

.. code-block:: rst

    .. figure:: /_static/example_scalebars.gif
        :align: center
        :alt: gallery_thumbnail

    This is a caption.

.. figure:: /_static/example_scalebars.gif
    :align: center
    :alt: gallery_thumbnail

    This is a caption.



figure directive without ``alt`` text
-------------------------------------

This figure directive does not have any ``alt`` text. Therefore, will not be
used as the thumbnail for the gallery.

.. code-block:: rst

    .. figure:: /_static/affine.png
        :align: center

        This is a caption.

.. figure:: /_static/affine.png
    :align: center

    This is a caption.
