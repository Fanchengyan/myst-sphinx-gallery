.. _example_order:

==========================
Controlling Examples Order
==========================

MyST Sphinx Gallery using files/directories order to determine the order of the gallery. To specify the order of the files/directories, you can add a number ``dd-`` prefix at the beginning of the file name. The number will be automatically removed from the file name in the output gallery.


For example, following files/directories order:

.. code-block:: bash

    examples
    ├── GALLERY_HEADER.rst
    ├── 02-basic
    │    ├── GALLERY_HEADER.rst
    │    ├── 01-basic-example3.rst
    │    ├── 02-basic-example2.md
    │    └── 03-basic-example1.ipynb
    └── 01-advanced
         ├── GALLERY_HEADER.rst
         ├── 01-advanced-example3.rst
         ├── 02-advanced-example2.md
         └── 03-advanced-example1.ipynb

will be displayed in the gallery as:

.. code-block:: bash

    auto_examples(index)
    ├── advanced(index)
    │    ├── advanced-example3
    │    ├── advanced-example2
    │    └── advanced-example1
    └── basic(index)
         ├── basic-example3
         ├── basic-example2
         └── basic-example1

