===================
Rst Image Directive
===================

This is a ``.rst`` file with ``image`` directive.
The example thumbnail is selected with ``image`` directive ``alt`` option
being set to ``gallery_thumbnail``.

image directive without ``alt`` text
------------------------------------

This ``image`` directive does not have any ``alt`` text. Therefore, will not be
used as the thumbnail for the gallery.

.. code-block:: rst

    .. image:: /_static/barchart.png
        :align: center

.. image:: /_static/barchart.png
    :align: center


image directive with ``alt`` text
---------------------------------

This ``image`` directive has set the ``alt`` attribute to ``gallery_thumbnail``.
Therefore, This image will be used as the thumbnail for the gallery.

.. code-block:: rst

    .. image:: /_static/example_scalebars.gif
        :align: center
        :alt: gallery_thumbnail

.. image:: /_static/example_scalebars.gif
    :align: center
    :alt: gallery_thumbnail



image directive without ``alt`` text
-------------------------------------

This ``image`` directive does not have any ``alt`` text. Therefore, will not be
used as the thumbnail for the gallery.

.. code-block:: rst

    .. image:: /_static/affine.png
        :align: center

.. image:: /_static/affine.png
    :align: center
