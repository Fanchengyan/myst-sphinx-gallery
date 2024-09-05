
.. _ref-gallery-example:

Using ref-gallery in Python Docs
================================

Here is an example demonstrating how to use the ``ref-gallery``
directive in your python code documentation.

.. code-block:: python
    :caption: myst_sphinx_gallery/directives.py
    :emphasize-lines: 4

    def gallery_example(self) -> None:
    """Serve as an example for the ``ref-gallery`` directive in code docs.

    .. ref-gallery::
        :tooltip:

        examples/alt/rst image
        examples/first_last/first
        examples/code_markdown/first code
    """

The documentation for this function will display a gallery as follows:

.. autofunction:: myst_sphinx_gallery.directives.RefGalleryDirective.gallery_example
    :noindex:
