"""
Patterns for the myst-sphinx-gallery extension.
"""

toc_gallery = """

.. toctree::
    :hidden:
"""

grid = """

.. grid:: 2 3 3 4
"""

grid_item_card = r"""
    .. grid-item-card:: :ref:`{target_ref}`
        :img-top: {img_path}
        :link: {target_ref}
        :link-type: ref
"""
