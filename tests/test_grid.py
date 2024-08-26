import pytest

from myst_sphinx_gallery.grid import (
    Grid,
    GridItemCard,
    TocTree,
    grid_item_card,
    param_to_str,
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
        assert grid.grid_args == "2 3 3 4"
        assert grid.gutter is None
        assert grid.margin is None
        assert grid.padding is None
        assert grid.outline is None
        assert grid.reverse is None
        assert grid.pattern == "\n\n.. grid:: 2 3 3 4\n\n"

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
        assert ":outline:" in grid.pattern
        assert ":reverse:" in grid.pattern

    def test_add_option(self):
        grid = Grid()
        grid.add_option("custom_option", 5)
        assert ":custom_option: 5" in grid.pattern

    def test_add_class_option(self):
        grid = Grid()
        grid.add_class_option("class-container", "class_test")
        assert "class_test" in list(grid.class_options.values())[0]

    def test_add_item(self):
        grid = Grid()
        grid.add_item("item1")
        assert grid.pattern == "\n\n.. grid:: 2 3 3 4\n\n    item1\n"
        grid.add_item("item2")
        assert grid.pattern == "\n\n.. grid:: 2 3 3 4\n\n    item1\n    item2\n"


class TestGridItemCard:
    def test_default_initialization(self):
        card = GridItemCard()
        print(card.pattern)
        assert card.columns is None
        assert card.margin is None
        assert card.padding is None

    def test_custom_initialization(self):
        card = GridItemCard(
            columns=6,
            margin=(2, 2, 1, 1),
            padding=(3, 1, 3, 1),
            width="auto",
            shadow="lg",
            border=1,
            rounded="circle",
            class_card="card_test",
            class_title="title_test",
        )
        print(card.pattern)
        assert ":columns: 6" in card.pattern
        assert ":margin: 2" in card.pattern
        assert ":padding: 3" in card.pattern
        assert ":width: auto" in card.pattern
        assert ":shadow: lg" in card.pattern
        assert "sd-border-1" in card.pattern
        assert "sd-rounded-circle" in card.pattern
        assert "card_test" in card.class_options["class-card"]
        assert "title_test" in card.class_options["class-title"]

    def test_add_option(self):
        card = GridItemCard()
        card.add_option("custom_option", 5)
        assert ":custom_option: 5" in card.pattern

    def test_add_class_option(self):
        card = GridItemCard()
        card.add_class_option("class-card", "class_test")
        assert "class_test" in list(card.class_options.values())[0]

    def test_add_item(self):
        card = GridItemCard()
        card.add_item("item1")
        assert "\n        item1\n" in card.pattern
        card.add_item("item2")
        assert "\n        item1\n        item2\n" in card.pattern

    def test_to_string(self):
        card = GridItemCard(columns=6, margin=2, padding=3)
        card.add_item("item1")
        card_str = card.to_string()
        assert ":columns: 6" in card_str
        assert ":margin: 2" in card_str
        assert ":padding: 3" in card_str
        assert "item1" in card_str

    def test_format(self):
        card = GridItemCard(columns=6, margin=2, padding=3)
        formatted_card = card.format(target_ref="ref1", img_path="path/to/img")
        assert ":columns: 6" in formatted_card
        assert ":margin: 2" in formatted_card
        assert ":padding: 3" in formatted_card
        assert ":ref:`ref1`" in formatted_card
        assert ":img-top: path/to/img" in formatted_card

    def test_copy(self):
        card = GridItemCard(columns=6, margin=2, padding=3)
        new_card = card.copy()
        assert new_card.columns == 6
        assert new_card.margin == 2
        assert new_card.padding == 3


class TestFormatParams:
    def test_with_tuple(self):
        assert param_to_str((1, 2, 3)) == "1 2 3"

    def test_with_list(self):
        assert param_to_str([1, 2, 3]) == "1 2 3"

    def test_with_string(self):
        assert param_to_str("test") == "test"

    def test_with_int(self):
        assert param_to_str(5) == "5"

    def test_with_bool(self):
        assert param_to_str(True) == "True"

    def test_with_invalid_type(self):
        with pytest.raises(ValueError):
            param_to_str({"key": "value"})
