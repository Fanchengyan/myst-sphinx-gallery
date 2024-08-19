===================
MyST Sphinx Gallery
===================

.. image:: https://img.shields.io/pypi/v/myst-sphinx-gallery
   :target: https://pypi.org/project/myst-sphinx-gallery/
   :alt: PyPI

.. image:: https://readthedocs.org/projects/myst-sphinx-gallery/badge/?version=latest
   :target: https://myst-sphinx-gallery.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://codecov.io/gh/Fanchengyan/myst-sphinx-gallery/graph/badge.svg?token=IHXYE1K1G9
   :target: https://codecov.io/gh/Fanchengyan/myst-sphinx-gallery
   :alt: Code Coverage

Introduction
------------

**MyST Sphinx Gallery** is a Sphinx extension that allows you to build galleries of examples from jupyter notebooks (``.ipynb``), markdown (``.md``) or reStructuredText (``.rst``) files. It works with ``MyST`` ecosystem, including `MyST-parser <https://myst-parser.readthedocs.io/en/latest/>`_ and `MyST-NB <https://myst-nb.readthedocs.io/en/latest/>`_, to render markdown or jupyter notebooks in Sphinx documentation.

Highlight Features
------------------

- **Convenient to use** - You can easily generate a gallery of examples from your Jupyter Notebooks, Markdown, or reStructuredText files. It works with ``MyST`` ecosystem, including `MyST-parser <https://myst-parser.readthedocs.io/en/latest/>`_ and `MyST-NB <https://myst-nb.readthedocs.io/en/latest/>`_, to render markdown or jupyter notebooks in Sphinx documentation.
- **Fast and robust** - It utilizes existing images to generate gallery thumbnails, eliminating code execution delays and potential accidental errors when building gallery.
- **Customizable** - You can customize the gallery, such as thumbnail selection, layout, and styling.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   user_guide/index
   examples
   api/index
   contributing/index
   changelog/index



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

      Learn how to use **MyST Sphinx Gallery** to generate a gallery for a well-structured examples folder.

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

      Explore the auto-generated examples from the examples folder.

      +++

      .. button-ref:: gallery_header
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
