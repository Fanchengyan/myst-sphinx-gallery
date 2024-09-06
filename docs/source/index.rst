===================
MyST Sphinx Gallery
===================

.. image:: https://img.shields.io/badge/recipe-myst--sphinx--gallery-green.svg
   :target: https://anaconda.org/conda-forge/myst-sphinx-gallery


.. image:: https://readthedocs.org/projects/myst-sphinx-gallery/badge/?version=latest
   :target: https://myst-sphinx-gallery.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/conda/vn/conda-forge/myst-sphinx-gallery.svg
   :target: https://anaconda.org/conda-forge/myst-sphinx-gallery

.. image:: https://img.shields.io/pypi/v/myst-sphinx-gallery
   :target: https://pypi.org/project/myst-sphinx-gallery/

.. image:: https://img.shields.io/conda/dn/conda-forge/myst-sphinx-gallery.svg
   :target: https://anaconda.org/conda-forge/myst-sphinx-gallery

.. image:: https://github.com/Fanchengyan/myst-sphinx-gallery/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/Fanchengyan/myst-sphinx-gallery/actions/workflows/tests.yml

.. image:: https://codecov.io/gh/Fanchengyan/myst-sphinx-gallery/graph/badge.svg?token=IHXYE1K1G9
   :target: https://codecov.io/gh/Fanchengyan/myst-sphinx-gallery


Introduction
------------

**MyST Sphinx Gallery** is a Sphinx extension that allows you to build
galleries from jupyter notebooks (``.ipynb``), markdown (``.md``) or
reStructuredText (``.rst``) files.

This extension is functionally similar to the
`Sphinx-Gallery <https://sphinx-gallery.github.io/stable/index.html>`_
extension, but aim to provide a simple and efficient way to create
galleries written in a variety of formats.

Highlight Features
------------------

- **Easy to use** - It provides a set of directives to generate
  galleries, as simple as adding ``toctree``.
- **Flexible** - You can easily generate a gallery of examples from your
  Jupyter Notebooks, Markdown, or reStructuredText files. It works with
  ``MyST`` ecosystem, including `MyST-parser <https://myst-parser.readthedocs.io/en/latest/>`_ and `MyST-NB <https://myst-nb.readthedocs.io/en/latest/>`_, to render markdown or jupyter notebooks in Sphinx documentation.
- **Fast and robust** - It utilizes existing images to generate gallery
  thumbnails, eliminating code execution delays and potential accidental errors
  when building gallery.
- **Customizable** - You can customize the gallery, such as thumbnail
  selection, and style of the gallery.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   user_guide/index
   examples/index
   api/index
   contributing/index
   About <about/index>



Navigation
----------

.. grid:: 1 2 2 2
   :gutter: 5
   :class-container: sd-text-center
   :padding: 5


   .. grid-item-card:: Quick Start
      :img-top: /_static/doc_index/index_get_start.svg
      :class-card: intro-card
      :shadow: md

      Learn how to install and use **MyST Sphinx Gallery** to generate galleries, and customize it.

      +++

      .. button-ref:: quick_start
         :ref-type: ref
         :click-parent:
         :color: warning
         :expand:

         To the Quick Start

   .. grid-item-card:: Gallery Example
      :img-top: /_static/doc_index/index_example.svg
      :class-card: intro-card
      :shadow: md

      Explore the Demo Gallery, showcasing gallery directives, thumbnail selection strategies, and options effects.

      +++

      .. button-ref:: demo_gallery
         :ref-type: ref
         :click-parent:
         :color: warning
         :expand:

         To the Gallery Example

   .. grid-item-card:: API Reference
      :img-top: /_static/doc_index/index_api.svg
      :class-card: intro-card
      :shadow: md

      Detailed API documentation for MyST Sphinx Gallery.

      +++

      .. button-ref:: api
         :ref-type: ref
         :click-parent:
         :color: warning
         :expand:

         To the API Reference

   .. grid-item-card::  Developer Guide
      :img-top: /_static/doc_index/index_contribute.svg
      :class-card: intro-card
      :shadow: md

      Do you want to contribute to MyST Sphinx Gallery? Check out the contributing guide.

      +++

      .. button-ref:: contributing
         :ref-type: ref
         :click-parent:
         :color: warning
         :expand:

         To the Contributing Guide
