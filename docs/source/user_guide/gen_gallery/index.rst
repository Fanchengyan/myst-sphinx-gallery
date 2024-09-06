.. _gen_gallery_method:

Generating Galleries Methods
============================

There are two ways to generate galleries in MyST Sphinx Gallery:

1. **Using directives:** MyST Sphinx Gallery provides three directives for
   generating galleries: ``base-gallery``, ``gallery``, and ``ref-gallery``.
   You can directly use these directives to generate galleries in
   reStructuredText (``.rst``), Markdown (``.md``), and Jupyter Notebook
   (``.ipynb``) files.
2. **Configuring in conf.py:** You can also generate gallery by specifying
   the examples and gallery directories in your ``conf.py`` file. This method
   is keeping in line with
   `Sphinx Gallery <https://sphinx-gallery.github.io/stable/index.html>`_
   extension.

.. note::

    **Using directives** is highly recommended for generating galleries
    as it provides more options and flexibility. For instance, you can
    add ``tooltip`` to example cards, **call different directives multi-times
    in a single file** to generate a complex gallery. This cannnot be
    done using the configuration method.


.. toctree::
    :maxdepth: 2

    directive/index
    conf/index
