.. _config_options:

=======================
Configuration Variables
=======================

MyST Sphinx Gallery has two main configuration variables that can be set in
your ``conf.py`` file.

- ``myst_sphinx_gallery_config`` : **global configuration** for all examples
  using gallery directives or used to **generate galleries**.
- ``myst_sphinx_gallery_files_config`` : **configuration for individual files**
  to override the global configuration for those files.

.. hint::

    Those two variables are optional and can be omitted if you don't need to
    customize the behavior of MyST Sphinx Gallery.

``myst_sphinx_gallery_config``
------------------------------

This variable has two usages:

1. It can be used to **generate galleries** when providing the examples and
   galleries dictionaries.
2. It will serve as a **global configuration** for all examples using gallery
   directives. In this case, examples and galleries dictionaries can be None.

The ``myst_sphinx_gallery_config`` variable can either be a instance of
:class:`~myst_sphinx_gallery.config.GalleryConfig` class or a dictionary
with the same keys as the :class:`~myst_sphinx_gallery.config.GalleryConfig`
class.

.. hint::

    The :class:`~myst_sphinx_gallery.config.GalleryConfig` is recommended as
    it provides type hints, which can be helpful for IDEs and linters.

Specify the thumbnail selection strategies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``myst_sphinx_gallery_config`` can be used to specify the thumbnail selection
strategies for the gallery. More details can be found in the
:ref:`thumbnail_strategy`

Customizing the thumbnail style
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``myst_sphinx_gallery_config`` can be used to customize the thumbnail style.
More details can be found in the :ref:`thumbnail_style`


Remove thumbnail after build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, MyST Sphinx Gallery will clean up the thumbnail files after the
build is complete. You can disable this behavior by setting
``remove_thumbnail_after_build`` to ``False`` in your
``myst_sphinx_gallery_config`` variable.

This can be useful if you are frequently re-building the documentation to
save building time.

.. code-block:: python
    :caption: conf.py
    :emphasize-lines: 5

    from myst_sphinx_gallery import GalleryConfig

    myst_sphinx_gallery_config = GalleryConfig(
        ...,  # other configurations
        remove_thumbnail_after_build=False,
    )

``myst_sphinx_gallery_files_config``
------------------------------------

This variable is used to **override the global configuration** for individual
files. It should be a instance of
:class:`~myst_sphinx_gallery.config.FilesConfig` class.

There are two parameters that should be set in this class:

- ``named_config`` : a dictionary of named configurations. The keys of the
  dictionary are the names of the configurations and the values are instances
  of :class:`~myst_sphinx_gallery.config.GalleryThumbnailConfig` class.
- ``files_config`` : a dictionary of config name and corresponding file paths
  that can be used to apply the same configuration to multiple files.

.. code-block:: python
    :caption: conf.py
    :emphasize-lines: 4, 18

     from myst_sphinx_gallery import FilesConfig, GalleryThumbnailConfig

    myst_sphinx_gallery_files_config = FilesConfig(
        named_config={
            "first_md": GalleryThumbnailConfig(
                thumbnail_strategy="first", notebook_thumbnail_strategy="markdown"
            ),
            "first_code": GalleryThumbnailConfig(
                thumbnail_strategy="first", notebook_thumbnail_strategy="code"
            ),
            "last_md": GalleryThumbnailConfig(
                thumbnail_strategy="last", notebook_thumbnail_strategy="markdown"
            ),
            "last_code": GalleryThumbnailConfig(
                thumbnail_strategy="last", notebook_thumbnail_strategy="code"
            ),
        },
        files_config={
            "first_code": [
                "examples/code_markdown/first code.ipynb",
                ],
            "last_code": [
                "examples/code_markdown/last code.ipynb",
                ],
            "first_md": [
                "examples/code_markdown/first markdown.ipynb",
                "examples/first_last/first.rst",
                ],
            "last_md": [
                "examples/code_markdown/last markdown.ipynb",
                "examples/first_last/last.rst",
                ],
        },
    )
