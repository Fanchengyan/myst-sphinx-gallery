import pytest

from myst_sphinx_gallery.grid import (
    Grid,
    GridItemCard,
    TocTree,
    format_params,
    grid_item_card,
)


class TestTocTree:
    def test_default_initialization(self):
        toc_tree = TocTree()
        assert toc_tree.pattern == "\n\n.. toctree::\n    :hidden:\n\n"

    def test_add_item(self):
        toc_tree = TocTree()
        toc_tree.add_item("item1")
        assert toc_tree.pattern == "\n\n.. toctree::\n    :hidden:\n\n    item1\n"
        toc_tree.add_item("item2")
        assert (
            toc_tree.pattern
            == "\n\n.. toctree::\n    :hidden:\n\n    item1\n    item2\n"
        )

    def test_str_method(self):
        toc_tree = TocTree()
        assert str(toc_tree) == "\n\n.. toctree::\n    :hidden:\n\n"

    def test_repr_method(self):
        toc_tree = TocTree()
        assert repr(toc_tree) == "TocTree(\n\n.. toctree::\n    :hidden:\n\n)"


class TestGrid:
    def test_default_initialization(self):
        grid = Grid()
        print(grid.pattern)
        assert grid.grid_option == (2, 3, 3, 4)
        assert grid.gutter is None
        assert grid.margin is None
        assert grid.padding is None
        assert grid.outline is None
        assert grid.reverse is None
        assert grid.pattern == "\n\n.. grid:: 2 3 3 4\n"

    def test_custom_initialization(self):
        grid = Grid(gutter=2, margin=3, padding=4, outline=True, reverse=True)
        print(grid.pattern)
        assert grid.gutter == 2
        assert grid.margin == 3
        assert grid.padding == 4
        assert grid.outline is True
        assert grid.reverse is True
        assert ":gutter: 2" in grid.pattern
        assert ":margin: 3" in grid.pattern
        assert ":padding: 4" in grid.pattern
        assert ":outline: True" in grid.pattern
        assert ":reverse: True" in grid.pattern

    def test_add_option(self):
        grid = Grid()
        grid.add_option("custom_option", 5)
        assert ":custom_option: 5" in grid.pattern

    def test_add_item(self):
        grid = Grid()
        grid.add_item("item1")
        assert grid.pattern == "\n\n.. grid:: 2 3 3 4\n\nitem1\n"
        grid.add_item("item2")
        assert grid.pattern == "\n\n.. grid:: 2 3 3 4\n\nitem1\nitem2\n"


class TestGridItemCard:
    def test_default_initialization(self):
        card = GridItemCard()
        print(card.pattern)
        assert card.columns is None
        assert card.margin is None
        assert card.padding is None

    def test_custom_initialization(self):
        card = GridItemCard(columns=6, margin=2, padding=3)
        print(card.pattern)
        assert card.columns == 6
        assert card.margin == 2
        assert card.padding == 3
        assert ":columns: 6" in card.pattern
        assert ":margin: 2" in card.pattern
        assert ":padding: 3" in card.pattern

    def test_add_option(self):
        card = GridItemCard()
        card.add_option("custom_option", 5)
        assert ":custom_option: 5" in card.pattern

    def test_add_item(self):
        card = GridItemCard()
        card.add_item("item1")
        assert card.pattern == grid_item_card + "\n        item1\n"
        card.add_item("item2")
        assert card.pattern == grid_item_card + "\n        item1\n        item2\n"


class TestFormatParams:
    def test_with_tuple(self):
        assert format_params((1, 2, 3)) == "1 2 3"

    def test_with_list(self):
        assert format_params([1, 2, 3]) == "1 2 3"

    def test_with_string(self):
        assert format_params("test") == "test"

    def test_with_int(self):
        assert format_params(5) == "5"

    def test_with_bool(self):
        assert format_params(True) == "True"

    def test_with_invalid_type(self):
        with pytest.raises(ValueError):
            format_params({"key": "value"})
