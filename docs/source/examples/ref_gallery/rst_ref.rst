========================
ref-gallery in RST files
========================


This is an example of how to use the ``ref-gallery``
directive in a reStructuredText file.


.. code-block:: rst
    :caption: ref-gallery.rst

    .. ref-gallery::
        :tooltip:

        examples/alt/rst image
        examples/first_last/first
        examples/code_markdown/first code


.. ref-gallery::
    :tooltip:

    examples/alt/rst image
    examples/first_last/first
    examples/code_markdown/first code



.. note::
    This file does not contain any images, even though there
    is a ``ref-gallery`` directive, which displays the thumbnail
    images of the examples. Therefore, the default gallery image
    will be used.
