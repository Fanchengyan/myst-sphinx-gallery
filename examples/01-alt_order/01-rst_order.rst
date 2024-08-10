=========
Rst Image
=========

This is a ``.rst`` gallery example with image URLs in the rst file to test ``gallery_thumbnail``.

image directive without ``alt`` text
------------------------------------

.. code-block:: rst

    .. image:: /_static/barchart.png
        :align: center

.. image:: /_static/barchart.png
    :align: center

image directive with ``alt`` set to ``gallery_thumbnail``
---------------------------------------------------------

.. code-block:: rst
    :emphasize-lines: 3

    .. image:: /_static/bar_colors.png
        :align: center
        :alt: gallery_thumbnail

.. note::

    This image directive has set the ``alt`` attribute to ``gallery_thumbnail``. Therefore, This image will be used as the thumbnail for the gallery.

.. image:: /_static/bar_colors.png
    :align: center
    :alt: gallery_thumbnail

figure directive without ``alt`` text
-------------------------------------

.. code-block:: rst

    .. figure:: /_static/affine.png
        :align: center

        This is a caption.

.. figure:: /_static/affine.png
    :align: center

    This is a caption.
