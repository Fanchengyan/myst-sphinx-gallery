Using Directives
================

**MyST Sphinx Gallery** provides **three directives** to help you generate
galleries:

- **base-gallery:** Create a base gallery.
- **gallery:** Create a total gallery in which base galleries serve as sections.
- **ref-gallery:** Create a gallery which items are all references to external
  files.

.. hint::
   - ``base-gallery`` and ``gallery`` directives will create ``toctree`` nodes
     automatically. They can be called multi-times in the same document.
     You can combine them to create more complex galleries.
   - ``ref-gallery`` directive can be used in your Python docs to display the related
     examples directly. Here is an example: :ref:`ref-gallery-directive-in-code-docs`.



Features and options of directives
-----------------------------------

Each directive has its own set of options and features, which are described
below.

.. csv-table:: Gallery Directives Features
   :header: "Directive", "Create TocTree", "Create Thumbnails", "Items", "Items Referenced Path "

   ``base-gallery``, "Yes", "Yes", "Files of examples", "This file"
   ``gallery``, "Yes", "No", "Files containing ``base-gallery`` directives", "This file"
   ``ref-gallery``, "No", "No", "Files of examples", "Source directory (``conf.py``)"

.. csv-table:: Gallery Directives Options
   :header: "Option", "Description", "Supported Directives"

   ``tooltip``, "show tooltips for gallery cards when hovered over", "``base-gallery``, ``gallery``, ``ref-gallery``"
   ``caption``, "Caption for the gallery (will be passed to the ``toctree`` directive)", "``base-gallery``, ``gallery``"

.. note::
   The ``tooltip`` is abstracted from the first paragraph below the title.
   Make sure to add a brief description in the first paragraph of the gallery
   file if you want to use the tooltip feature.

Usages of directives for different file types
---------------------------------------------

.. hint::
   :ref:`demo_gallery` are some examples demonstrating the usage of the
   gallery directives, thumbnail selection strategies, effects of options.
   You can click the ``Code for this gallery`` above the gallery cards
   to see the source code.


reStructuredText
~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. base-gallery::
      :caption: Gallery Caption
      :tooltip:

      example file1
      example file2
      example file3


   .. gallery::
      :caption: Gallery Caption
      :tooltip:

      file1 containing base-gallery directive
      file2 containing base-gallery directive
      file3 containing base-gallery directive

   .. ref-gallery::
      :tooltip:

      source/path/to/example file1
      source/path/to/example file2
      source/path/to/example file3

markdown/jupyter notebook
~~~~~~~~~~~~~~~~~~~~~~~~~

Both ``backticks`` and ``colons`` code fences are supported for the directives.

Here is the usage of the directives in ``backticks`` code fences for those
three gallery directives:

.. code-block:: markdown

   ```{base-gallery}
   :caption: Gallery Caption
   :tooltip:

   example file1
   example file2
   example file3
   ```

    ```{gallery}
    :caption: Gallery Caption
    :tooltip:

   file1 containing base-gallery directive
   file2 containing base-gallery directive
   file3 containing base-gallery directive
   ```


   ```{ref-gallery}
   :tooltip:

   source/path/to/example file1
   source/path/to/example file2
   source/path/to/example file3
   ```

Following is the usage of the directives in ``colons`` code fences for those
three gallery directives:

.. code-block:: markdown


   :::{gallery}
   :caption: Gallery Caption
   :tooltip:

   file1 containing base-gallery directive
   file2 containing base-gallery directive
   file3 containing base-gallery directive
   :::

   :::{base-gallery}
   :caption: Gallery Caption
   :tooltip:

   example file1
   example file2
   example file3
   :::


   :::{ref-gallery}
   :tooltip:

   source/path/to/example file1
   source/path/to/example file2
   source/path/to/example file3
   :::

.. note::
   To enable the ``colons`` code fences, you need to enable the ``colon_fence``
   option in your ``conf.py`` file. For more information, see:
   `Code fences using colons <https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons>`_.

.. _ref-gallery-directive-in-code-docs:

Using ``ref-gallery`` in code docs
----------------------------------

You can directly add the ``ref-gallery`` directive in your Python code docs.

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
