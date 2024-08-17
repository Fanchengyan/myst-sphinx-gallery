"""
Patterns for the myst-sphinx-gallery extension.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

grid_item_card = r"""
    .. grid-item-card:: :ref:`{target_ref}`
        :img-top: {img_path}
        :link: {target_ref}
        :link-type: ref
"""


class TocTree:
    """
    A class to create a table of content for the gallery images.
    """

    def __init__(self, pattern: str | None = None):
        if pattern:
            self.pattern = pattern
        else:
            self.pattern = "\n\n.. toctree::\n    :hidden:\n\n"

    def __str__(self) -> str:
        return self.pattern

    def __repr__(self) -> str:
        return f"TocTree({self.pattern})"

    def add_item(self, item: str):
        """Add an item to the table of content."""
        self.pattern += f"    {item}\n"

    def parse_item(self, file_path: Path, ref_dir: Path) -> str:
        """Parse the item for the table of content from the file path.

        Parameters
        ----------
        file_path : Path
            The file path of the item.
        ref_dir : Path
            The reference directory for the item.
        """
        item = file_path.relative_to(ref_dir).with_suffix("").as_posix()
        return item

    def copy(self) -> TocTree:
        """Return a new instance of the TocTree class.

        .. note:: The new instance will only have the same options, but no items.
        """
        return TocTree("\n\n.. toctree::\n    :hidden:\n\n")


@dataclass
class Grid:
    """
    A class to create a grid pattern by given parameters. Detailed explanation of
    the parameters can be found in the
    `grid options <https://sphinx-design.readthedocs.io/en/latest/grids.html#grid-options>`_.
    """

    #: The number of columns in the grid for each breakpoint (xs sm md lg).
    #: Detailed explanation of the breakpoints can be found in the
    #: `Bootstrap Breakpoint <https://getbootstrap.com/docs/5.0/layout/breakpoints/>`_.
    grid_option: int | tuple[int] = (2, 3, 3, 4)

    #: Spacing between items.
    gutter: Literal[0, 1, 2, 3, 4, 5] | tuple[int] | None = None

    #: Outer margin of grid.
    margin: Literal[0, 1, 2, 3, 4, 5, "auto"] | tuple[int] | None = None

    #: Inner padding of grid.
    padding: Literal[0, 1, 2, 3, 4, 5] | tuple[int] | None = None

    #: Create a border around the grid.
    outline: bool | None = None

    #: Reverse the order of the grid items.
    reverse: bool | None = None

    def __post_init__(self):
        self.pattern = f"\n\n.. grid:: {format_params(self.grid_option)}\n"
        self._no_items = True
        self.options = {}

        if self.gutter:
            self.add_option("gutter", self.gutter)
        if self.margin:
            self.add_option("margin", self.margin)
        if self.padding:
            self.add_option("padding", self.padding)
        if self.outline:
            self.add_option("outline", self.outline)
        if self.reverse:
            self.add_option("reverse", self.reverse)

    def __str__(self) -> str:
        return self.pattern

    def __repr__(self) -> str:
        return f"Grid({self.pattern})"

    def add_option(self, option: str, value: Any):
        """Add an option to the grid item card pattern."""
        self.options[option] = value
        self.pattern += f"    :{option}: {format_params(value)}\n"

    def add_item(self, item: GridItemCard | str):
        """Add an item to the grid pattern."""
        if self._no_items:
            # add two new lines before the first item
            self.pattern += f"\n{item}\n"
            self._no_items = False
        else:
            self.pattern += f"{item}\n"

    def copy(self) -> Grid:
        """Return a new instance of Grid with same options.

        .. note:: The new instance will only have the same options, but no items.
        """
        grid = Grid(grid_option=self.grid_option)
        for option, value in self.options.items():
            grid.add_option(option, value)

        return grid


@dataclass
class GridItemCard:
    """
    A class to create a grid item card pattern by given parameters. Detailed explanation of the parameters can be found in the `grid item card options <https://sphinx-design.readthedocs.io/en/latest/grids.html#grid-item-card-options>`_.
    """

    #: The number of columns (out of 12) a grid-item will take up.
    columns: int | tuple[int] | None = None

    #: Outer margin of grid item.
    margin: Literal[0, 1, 2, 3, 4, 5, "auto"] | tuple[int] | None = None

    #: Inner padding of grid item.
    padding: Literal[0, 1, 2, 3, 4, 5] | tuple[int] | None = None

    def __post_init__(self):
        self.pattern = grid_item_card
        self._no_items = True
        self.options = {}

        if self.columns:
            self.add_option("columns", self.columns)
        if self.margin:
            self.add_option("margin", self.margin)
        if self.padding:
            self.add_option("padding", self.padding)

    def __str__(self) -> str:
        return self.pattern

    def __repr__(self) -> str:
        return f"GirdItemCard({self.pattern})"

    def add_option(self, option: str, value: Any):
        """Add an option to the grid item card pattern."""
        self.options[option] = value
        self.pattern += f"        :{option}: {format_params(value)}\n"

    def add_item(self, item: str):
        """Add an item to the grid item card pattern."""
        if self._no_items:
            # add two new lines before the first item
            self.pattern += f"\n        {item}\n"
            self._no_items = False
        else:
            self.pattern += f"        {item}\n"

    def format(self, target_ref: str, img_path: str) -> str:
        """Format the grid item card pattern with the target reference and image path."""
        return self.pattern.format(target_ref=target_ref, img_path=img_path)

    def copy(self) -> GridItemCard:
        """Return a new instance of GridItemCard with same options.

        .. note:: The new instance will only have the same options, but no items.
        """
        card = GridItemCard()
        card.pattern = grid_item_card
        for option, value in self.options.items():
            card.add_option(option, value)
        return card


def format_params(parameter: Any) -> str:
    """Format the grid or card parameters."""
    if isinstance(parameter, (tuple, list)):
        return " ".join(map(str, parameter))
    if not isinstance(parameter, (str, int, bool)):
        raise ValueError(f"{parameter} cannot be {type(parameter)}")
    return str(parameter)
