"""Patterns for the myst-sphinx-gallery extension."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pathlib import Path

grid_item_card = r"""
    .. grid-item-card:: :ref:`{target_ref}`
        :img-top: {img_path}
        :link: {target_ref}
        :link-type: ref
"""

grid_classes = [
    "class-container",
    "class-row",
]

card_classes = [
    "class-item",
    "class-card",
    "class-title",
    "class-header",
    "class-body",
    "class-footer",
    "class-img-top",
    "text-align",
]

card_classes_invalid = [
    "class-img-bottom",
]

class_options = grid_classes + card_classes + card_classes_invalid


class TocTree:
    """A class to create a table of content for the gallery images."""

    def __init__(self, pattern: str | None = None) -> None:
        """Initialize the TocTree class."""
        if pattern:
            self._pattern = pattern
        else:
            self._pattern = "\n\n.. toctree::\n    :hidden:\n\n"

    def __str__(self) -> str:
        """Return the table of content pattern."""
        return self._pattern

    def __repr__(self) -> str:
        """Return the table of content pattern."""
        return f"TocTree({self._pattern})"

    def add_item(self, item: str) -> None:
        """Add an item to the table of content."""
        self._pattern += f"    {item}\n"

    @property
    def pattern(self) -> str:
        """Return the table of content pattern."""
        return self._pattern

    def parse_item(self, file_path: Path, ref_dir: Path) -> str:
        """Parse the item for the table of content from the file path.

        Parameters
        ----------
        file_path : Path
            The file path of the item.
        ref_dir : Path
            The reference directory for the item.

        """
        return file_path.relative_to(ref_dir).with_suffix("").as_posix()

    def copy(self) -> TocTree:
        """Return a new instance of the TocTree class.

        .. note:: The new instance will only have the same options, but no items.
        """
        return TocTree("\n\n.. toctree::\n    :hidden:\n\n")


@dataclass
class Grid:
    """A class to create a grid pattern by given parameters.

    Detailed explanation of the parameters can be found in the
    `grid options <https://sphinx-design.readthedocs.io/en/latest/grids.html#grid-options>`_.
    """

    #: Create a border around the grid.
    outline: bool | None = None

    #: Reverse the order of the grid items.
    reverse: bool | None = None

    #: Additional CSS classes for the grid container element.
    class_container: str | list[str] | None = None

    #: Additional CSS classes for the grid row element.
    class_row: str | list[str] | None = None

    def __post_init__(self) -> None:
        """Post initialization of the Grid class."""
        self._pattern = "\n\n.. grid::\n"
        self._no_items = True
        self.options = {}
        self.class_options = {}
        self.options_format = {}
        self.items = []

        # add myst-sphinx-gallery class options
        self.add_class_option("class-container", "msg-sd-container")
        self.add_class_option("class-row", "msg-sd-row")

        if self.outline:
            self.add_option("outline", "")
        if self.reverse:
            self.add_option("reverse", "")
        if self.class_container is not None:
            self.add_option("class-container", self.class_container)
        if self.class_row is not None:
            self.add_option("class-row", self.class_row)

    def __str__(self) -> str:
        """Return the grid pattern string."""
        return self.to_string()

    def __repr__(self) -> str:
        """Return the grid pattern string."""
        return f"Grid({self.to_string()})"

    def add_option(self, option: str, value: object) -> None:
        """Add an option to the grid item card pattern."""
        if option in grid_classes:
            self.add_class_option(option, value)
            return

        self.options[option] = value
        self.options_format.update({option: param_to_str(value)})

    def add_class_option(self, option: str, value: str) -> None:
        """Add class option to the grid pattern."""
        if option not in grid_classes:
            msg = f"{option} is a valid class option for grid."
            warnings.warn(msg, stacklevel=2)
            self.add_option(option, value)
            return
        if option not in self.class_options:
            self.class_options[option] = set()
        self.class_options[option] = self.class_options[option].union(
            set(param_to_str(value).split(" "))
        )
        self.options[option] = value

    def add_item(self, item: GridItemCard | str) -> None:
        """Add an item to the grid pattern."""
        self.items.append(item)

    @property
    def pattern(self) -> str:
        """Return the grid item card pattern string.

        This property is a alias for the `to_string` method.
        """
        return self.to_string()

    def to_string(self) -> str:
        """Return the grid pattern string."""
        pattern = self._pattern
        # add options to the pattern
        for key, value in self.options_format.items():
            pattern += f"    :{key}: {value}\n"
        # add classes options to the pattern
        for key, value in self.class_options.items():
            pattern += f"    :{key}: {' '.join(value)}\n"
        # add items to the pattern
        items_str = "\n"
        for item in self.items:
            items_str += f"    {item}\n"
        pattern += items_str

        return pattern

    def copy(self) -> Grid:
        """Return a new instance of Grid with same options.

        .. note:: The new instance will only have the same options, but no items.
        """
        new_grid = Grid(
            outline=self.outline,
            reverse=self.reverse,
            class_container=self.class_container,
            class_row=self.class_row,
        )
        new_grid.options = self.options.copy()
        new_grid.class_options = self.class_options.copy()
        new_grid.options_format = self.options_format.copy()
        return new_grid


@dataclass
class GridItemCard:
    """A class to create a grid item card pattern by given parameters.

    Detailed explanation of the parameters can be found in the
    `card options <https://sphinx-design.readthedocs.io/en/pydata-theme/cards.html#card-options>`_.
    and `grid item card <https://sphinx-design.readthedocs.io/en/pydata-theme/grids.html#grid-item-card-options>`_.
    """

    #: Additional CSS classes for the grid row element.
    width: Literal["25%", "50%", "75%", "100%", "auto"] | None = None

    #: Default horizontal text alignment: left, right, center or justify
    text_align: Literal["left", "right", "center", "justify"] = "center"

    #: The size of the shadow below the card: none, sm (default), md, lg.
    shadow: Literal["none", "sm", "md", "lg"] = "md"

    #: The border width of the card: 0, 1, 2, 3, 4, 5 or
    #: a tuple of four integers for (top bottom left right).
    border: Literal[0, 1, 2, 3, 4, 5] | tuple[int, int, int, int] = 0

    #: The border radius of the card: 0, 1, 2, 3, "circle", "pill".
    rounded: Literal[0, 1, 2, 3, "circle", "pill"] = 2

    #: Additional CSS classes for the card container element.
    class_card: str | list[str] | None = None

    #: Additional CSS classes for the title element.
    class_title: str | list[str] | None = None

    #: Additional CSS classes for the top image
    class_img_top: str | list[str] | None = None

    #: Additional CSS classes for the card image element.
    class_header: str | list[str] | None = None

    #: Additional CSS classes for the body element.
    class_body: str | list[str] | None = None

    #: Additional CSS classes for the footer element.
    class_footer: str | list[str] | None = None

    def __post_init__(self) -> None:
        """Post initialization of the GridItemCard class."""
        self._pattern: str = grid_item_card
        self._no_items: bool = True
        self.options: dict[str, object] = {}
        self.class_options: dict[str, set] = {}
        self.options_format: dict[str] = {}
        self.items: list = []

        # add myst-sphinx-gallery class options
        self.add_class_option("class-card", "msg-sd-card")
        self.add_class_option("class-item", "msg-sd-card-hover")
        self.add_class_option("class-title", "msg-sd-card-title")
        self.add_class_option("class-img-top", "msg-sd-card-img-top")
        self.add_class_option("class-header", "msg-sd-card-header")
        self.add_class_option("class-body", "msg-sd-card-body")
        self.add_class_option("class-footer", "msg-sd-card-footer")

        # Auxiliary options
        if self.width is not None:
            self.add_option("width", self.width)
        self.add_option("shadow", self.shadow)
        # Auxiliary class options
        self.add_class_option("class-card", f"sd-border-{self.border}")
        self.add_class_option("class-card", f"sd-rounded-{self.rounded}")
        self.add_class_option("text-align", self.text_align)
        if self.class_card is not None:
            self.add_class_option("class-card", self.class_card)
        if self.class_title is not None:
            self.add_class_option("class-title", self.class_title)
        if self.class_img_top is not None:
            self.add_class_option("class-img-top", self.class_img_top)
        if self.class_header is not None:
            self.add_class_option("class-header", self.class_header)
        if self.class_body is not None:
            self.add_class_option("class-body", self.class_body)
        if self.class_footer is not None:
            self.add_class_option("class-footer", self.class_footer)

    def __str__(self) -> str:
        """Return the grid item card pattern string."""
        return self.to_string()

    def __repr__(self) -> str:
        """Return the grid item card pattern string."""
        return f"GirdItemCard({self.to_string()})"

    def add_option(self, option: str, value: object) -> None:
        """Add an option to the grid item card pattern."""
        if option in card_classes:
            self.add_class_option(option, value)
            return
        self.options_format.update({option: param_to_str(value)})
        self.options[option] = value

    def add_class_option(self, option: str, value: str) -> None:
        """Add class option to the grid item card pattern."""
        if option not in card_classes:
            msg = f"{option} is not a valid class option for grid item card."
            warnings.warn(msg, stacklevel=2)
            self.add_option(option, value)
        if option in card_classes_invalid:
            msg = f"{option} is not suggested in myst-sphinx-gallery."
            warnings.warn(msg, stacklevel=2)

        if option not in self.class_options:
            self.class_options[option] = set()
        self.class_options[option] = self.class_options[option].union(
            set(param_to_str(value).split(" "))
        )
        self.options[option] = value

    def add_item(self, item: str) -> None:
        """Add an item to the grid item card pattern."""
        self.items.append(item)

    @property
    def pattern(self) -> str:
        """Return the grid item card pattern string.

        This property is a alias for the `to_string` method.
        """
        return self.to_string()

    def to_string(self) -> str:
        """Return the grid item card pattern string."""
        pattern = self._pattern
        # add options to the pattern
        for key, value in self.options_format.items():
            pattern += f"        :{key}: {value}\n"
        # add classes options to the pattern
        for key, value in self.class_options.items():
            pattern += f"        :{key}: {' '.join(value)}\n"
        # add items to the pattern
        items_str = "\n"
        for item in self.items:
            items_str += f"        {item}\n"
        pattern += items_str
        # add options to the pattern

        return pattern

    def format(self, target_ref: str, img_path: str) -> str:
        """Format grid item card pattern with target reference and image path."""
        return self.to_string().format(target_ref=target_ref, img_path=img_path)

    def copy(self) -> GridItemCard:
        """Return a new instance of GridItemCard with same options.

        .. note:: The new instance will only have the same options, but no items.
        """
        new_card = GridItemCard(
            width=self.width,
            text_align=self.text_align,
            shadow=self.shadow,
            border=self.border,
            rounded=self.rounded,
            class_card=self.class_card,
            class_title=self.class_title,
            class_img_top=self.class_img_top,
            class_header=self.class_header,
            class_body=self.class_body,
            class_footer=self.class_footer,
        )
        new_card.options = self.options.copy()
        new_card.class_options = self.class_options.copy()
        new_card.options_format = self.options_format.copy()
        return new_card


def param_to_str(parameter: object) -> str:
    """Format the grid or card parameters."""
    if isinstance(parameter, (tuple, list, set)):
        return " ".join(map(str, parameter))
    if not isinstance(parameter, (str, int, bool)):
        msg = f"{parameter} cannot be {type(parameter)}"
        raise TypeError(msg)
    return str(parameter)
