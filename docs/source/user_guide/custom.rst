
.. _custom:

=======================================
Customizing Style of Thumbnail and Card
=======================================

This page demonstrates how to customize the thumbnail and card style of gallery
examples in the MyST Sphinx Gallery.


.. _thumbnail_style:

Customizing thumbnail style
---------------------------

By default, the thumbnails will be resized to (320, 224) pixels with a ``pad``
operation to white background color. You can customize the thumbnail
behavior by providing a different configuration to the
:class:`~myst_sphinx_gallery.config.ThumbnailConfig` class.

For example, you can change the thumbnail size to (320, 320) pixels with a
``pad`` operation and a orange background color by adding the following code in
the ``conf.py`` file:

.. code-block:: python
    :caption: conf.py

    from myst_sphinx_gallery import GalleryConfig, ThumbnailConfig

    myst_sphinx_gallery_config = GalleryConfig(
        ..., # other configurations
        thumbnail_config=ThumbnailConfig(
            ref_size=(320, 320),
            operation="pad",
            operation_kwargs={"color": "orange"},
            quality_static=90,
        ),
    )


Customizing card style using CSS
--------------------------------

You can also customize the card style using CSS. The MyST Sphinx Gallery uses
CSS variables to define the style of the card. You can override these variables
by defining new values in your custom CSS file.


.. tip::

    To override the default CSS variables, you can define new values in your
    custom CSS file and include it in the ``html_css_files`` list in your
    ``conf.py`` file.

    .. code-block:: python
        :caption: conf.py

        html_static_path = ["_static"]
        html_css_files = ["custom.css"]

Here is the default CSS variables:

.. code-block:: css
    :caption: myst_sphinx_gallery.css

    :root {
        --msg-title-font-size: 1.0rem;
        --msg-box-border-radius: 0.3rem;
        --msg-box-min-width: 160px;
        --msg-box-max-width: 1fr;

    }

    :root,
    html[data-theme=light],
    body[data-theme=light] {
        --msg-tooltip-foreground: black;
        --msg-tooltip-background: rgba(250, 250, 250, 0.9);
        --msg-tooltip-border: #ccc transparent;
        --msg-box-background-color: #ffffff7a;
        --msg-box-shadow-color: #6c757d40;
        --msg-box-hover-shadow-color: #06060640;
        --msg-box-hover-border-color: #0069d9;
        --msg-box-hover-border-width: 1px;
        --msg-font-color-title: black;
    }

    @media(prefers-color-scheme: light) {

        :root[data-theme=auto],
        html[data-theme=auto],
        body[data-theme=auto] {
            --msg-tooltip-foreground: black;
            --msg-tooltip-background: rgba(250, 250, 250, 0.9);
            --msg-tooltip-border: #ccc transparent;
            --msg-box-background-color: #ffffff7a;
            --msg-box-shadow-color: #6c757d40;
            --msg-box-hover-shadow-color: #06060640;
            --msg-box-hover-border-color: #0069d9;
            --msg-box-hover-border-width: 1px;
            --msg-font-color-title: black;
        }
    }

    :root,
    html[data-theme=dark],
    body[data-theme=dark] {
        --msg-tooltip-foreground: white;
        --msg-tooltip-background: rgba(10, 10, 10, 0.9);
        --msg-tooltip-border: #333 transparent;
        --msg-box-background-color: #9494947a;
        --msg-box-shadow-color: #79848d40;
        --msg-box-hover-shadow-color: #e6e6e640;
        --msg-box-hover-border-color: #003975;
        --msg-box-hover-border-width: 2px;
        --msg-font-color-title: white;
    }

    @media(prefers-color-scheme: dark) {

        html[data-theme=auto],
        body[data-theme=auto] {
            --msg-tooltip-foreground: white;
            --msg-tooltip-background: rgba(10, 10, 10, 0.9);
            --msg-tooltip-border: #333 transparent;
            --msg-box-background-color: #9494947a;
            --msg-box-shadow-color: #79848d40;
            --msg-box-hover-shadow-color: #e6e6e640;
            --msg-box-hover-border-color: #003975;
            --msg-box-hover-border-width: 2px;
            --msg-font-color-title: white;

        }
    }
