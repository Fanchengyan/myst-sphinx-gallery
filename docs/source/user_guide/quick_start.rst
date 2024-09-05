.. _quick_start:

===========
Quick Start
===========

This page gives a quick start guide of how to get started with MyST Sphinx Gallery.

Installation
------------

**MyST Sphinx Gallery** is a Python package, and requires ``Python >= 3.8``.
You can install the latest release using ``pip`` or ``conda`` / ``mamba``:

.. tab-set::

    .. tab-item:: pip

        .. code-block:: bash

            pip install myst-sphinx-gallery

    .. tab-item:: conda

        .. code-block:: bash

            conda install -c conda-forge myst-sphinx-gallery

    .. tab-item:: mamba

        .. code-block:: bash

            mamba install -c conda-forge myst-sphinx-gallery

Configuring the extension
-------------------------

Enable the extension
~~~~~~~~~~~~~~~~~~~~

After installation, you can enable the extension in Sphinx ``conf.py`` file:

.. code-block:: python
    :caption: conf.py

    extensions = [
        ...,  # other extensions
        "myst_sphinx_gallery",
    ]


.. important::

    **MyST Sphinx Gallery only helps you to generate the gallery**. You need to enable the MyST parsers to render the markdown or jupyter notebook files by yourself.

    For instance, to enable the MyST-NB, you can add the following code to the ``conf.py`` file:

    .. code-block:: python
        :caption: conf.py

        extensions = [
            ...,
            "myst_nb",
        ]

        source_suffix = {
            ".rst": "restructuredtext",
            ".md": "myst-nb",
            ".myst": "myst-nb",
        }

    For more information, please refer to the documentation of `MyST <https://myst-parser.readthedocs.io/en/latest/>`_ and `MyST-NB  <https://myst-nb.readthedocs.io/en/latest/>`_.


Configuring the variables
~~~~~~~~~~~~~~~~~~~~~~~~~

MyST Sphinx Gallery has two main configuration variables that can be set in
your ``conf.py`` file.

- ``myst_sphinx_gallery_config`` : **global configuration** for all examples
  using gallery directives or used to **generate galleries**.
- ``myst_sphinx_gallery_files_config`` : **configuration for individual files**
  to override the global configuration for those files.

.. hint::

    Those two variables are optional and can be omitted if you don't need to
    customize the behavior of MyST Sphinx Gallery.

More details about the configuration variables can be found in the
:ref:`config_options` section.

Generating gallery
------------------

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

You can refer to the :ref:`gen_gallery_method` section for more details.


Thumbnail selection strategy for examples
-----------------------------------------

.. hint::
    Here is a brief explanation of the thumbnail selection strategy for examples.
    More details can be found in the :ref:`thumbnail_strategy`.

- **one image** - If there only one image in an example file, no additional
  configuration is needed, and that image will be used as gallery thumbnail.
- **multiple images** - If there are multiple figures in an example file, you
  can specify the strategy to determine which thumbnail will be used for the
  gallery. The following strategies are supported:

  1. **alt** - If the alt attribute of an image/figure is set to
     ``gallery_thumbnail``, that image/figure will be used as the gallery
     thumbnail for this file.
  2. **first/last** - If there are multiple images that can be used as the
     gallery thumbnail, the first/last image will be selected. You can specify
     the strategy by setting the ``thumbnail_strategy`` in the configuration
     file. The default value is ``first``.
  3. **code/markdown** - For Jupyter notebook files, both markdown and code
     cells can contain images. You can specify the strategy by setting the
     ``notebook_thumbnail_strategy`` in the configuration file. The default
     value is ``code``.

- **no image** - If no image/figure is found, the default thumbnail will be used.


Customizing style of gallery
----------------------------

You can customize the style of the thumbnail and example cards. More details
can be found in the :ref:`custom` section.
