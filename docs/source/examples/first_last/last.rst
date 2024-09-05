=================
``last`` strategy
=================

This is a gallery example with image URLs in the ``.rst`` file to test
``last`` strategy. Since no ``alt`` attribute is set to
``gallery_thumbnail``, the last image in the file will be used as the
thumbnail for the gallery.


.. code-block:: rst

    .. image:: /_static/intersecting_planes.png
        :align: center
        :width: 60%

.. image:: /_static/intersecting_planes.png
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

    .. figure:: /_static/offset.png
        :align: center
        :width: 60%

        This is a caption.

.. figure:: /_static/offset.png
    :align: center
    :width: 60%

    This is a caption.
