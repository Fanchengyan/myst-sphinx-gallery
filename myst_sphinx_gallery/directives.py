"""Sphinx directives to generate galleries."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal, Sequence

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.directives.other import TocTree
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx_design.cards import CardDirective
from sphinx_design.shared import PassthroughTextElement

from .config import GalleryConfig, GalleryThumbnailConfig
from .gallery import ExampleConverter
from .grid import Grid, GridItemCard
from .utils import (
    extract_title_and_tooltip,
    get_base_gallery_items,
    parse_files_without_suffix,
    remove_special_chars,
)

logger = logging.getLogger(__name__)


class GalleryABC(SphinxDirective):
    """An abstract class for the gallery directives."""

    def run(self) -> list[nodes.Node]:
        """Generate the gallery nodes."""
        raise NotImplementedError

    def create_cards_for_row_node(
        self,
        entry_files: str,
        row_node: nodes.Node,
        save_thumbnail: bool,
    ) -> nodes.Node:
        """Create the cards for the row node."""
        docname = self.env.docname
        src_dir = self.env.app.srcdir

        for entry_file in entry_files:
            gallery_config = self.parse_file_gallery_config(entry_file)

            entry_rel = entry_file.relative_to(src_dir).with_suffix("").as_posix()

            # Create a reference node
            reference = nodes.reference("", f"{entry_rel}")
            reference["internal"] = True
            ref_url = self.env.app.builder.get_relative_uri(docname, entry_rel)
            reference["refuri"] = ref_url

            # Generate the thumbnail for this example
            conv = ExampleConverter(
                entry_file,
                gallery_config.examples_dirs[0],
                gallery_config.gallery_dirs[0],
                config=gallery_config,
                thumbnail_location="parent",
                save_thumbnail=save_thumbnail,
            )
            conv._parse_thumb()

            # configure the card
            grid_item_card = GridItemCard()
            grid_item_card.add_option("img-top", conv.gallery_thumb)
            grid_item_card.add_option("link", ref_url)
            grid_item_card.add_option("link-type", "url")
            if "tooltip" in self.options:
                grid_item_card.add_class_option("class-item", "msg-tooltip")
            options_card = grid_item_card.options_format.copy()

            options_card.update(
                {key: list(val) for key, val in grid_item_card.class_options.items()}
            )

            title, tooltip = extract_title_and_tooltip(entry_file)
            title = remove_special_chars(title)
            tooltip = remove_special_chars(tooltip)

            # update nodes
            card_node = create_card_node(grid_item_card.items, options_card, self)
            card_node["tooltip"] = tooltip
            title_node = create_card_title_node(title)
            for child in card_node.children[0]:
                if "sd-card-body" in child["classes"]:
                    child.insert(0, title_node)
                    break

            row_node += card_node

        return row_node

    def create_toctree(self) -> list[nodes.Node]:
        """Generate the toctree node for the sub-gallery."""
        options = {
            "hidden": True,
            "includehidden": True,
        }
        caption = self.options.get("caption", None)
        if caption:
            options["caption"] = caption

        toctree = TocTree(
            "toctree",
            [],
            options,
            content=self.content,
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        )
        return toctree.run()

    def parse_file_gallery_config(self, file_path: str) -> GalleryConfig:
        """Parse the gallery config for give file."""
        path_relative = Path(file_path).relative_to(self.env.app.srcdir).as_posix()
        config = self.env.config
        if (
            hasattr(config, "myst_sphinx_gallery_files_config")
            and config.myst_sphinx_gallery_files_config
        ):
            files_config = config.myst_sphinx_gallery_files_config
            gallery_config = ensure_config(files_config.get(path_relative))
        elif (
            hasattr(config, "myst_sphinx_gallery_config")
            and config.myst_sphinx_gallery_config
        ):
            gallery_config = ensure_config(config.myst_sphinx_gallery_config)
        else:
            gallery_config = GalleryConfig()

        # update the gallery config with the directive defaults
        config_dict = gallery_config.to_dict()
        config_dict.update(
            {
                "examples_dirs": "./",
                "gallery_dirs": "./",
                "root_dir": self.env.app.srcdir,
                "base_gallery": True,
            }
        )
        return GalleryConfig(**config_dict)


class RefGalleryDirective(GalleryABC):
    """Directive to create a referenced gallery using ``ref-gallery`` directive.

    This gallery will not create toctree entries for the examples. The
    examples in this gallery are all referenced from other galleries.
    """

    option_spec = {"tooltip": directives.flag}  # noqa: RUF012
    has_content = True

    def run(self) -> list[nodes.Node]:
        """Generate the grid node for the ``ref-gallery`` directive."""
        src_dir = self.env.app.srcdir
        docname = self.env.docname

        grid_node, row_node = create_grid_node(Grid(), self)
        for entry in self.content:
            if not entry:
                continue
            # Resolve the path relative to the current document
            entry_path = Path(src_dir) / entry
            try:
                entry_files = parse_files_without_suffix(entry_path)
                self.create_cards_for_row_node(
                    entry_files, row_node, save_thumbnail=True
                )
            except Exception as exc:
                msg = f"Error in directive '{self.name}' in document '{docname}': {exc}"
                logger.exception(msg)
                self.error(msg)
        grid_node += row_node

        return [grid_node]

    def gallery_example(self) -> None:
        """Serve as an example for the ``ref-gallery`` directive in code docs.

        .. ref-gallery::
            :tooltip:

            examples/alt/rst image
            examples/first_last/first
            examples/code_markdown/first code

        """
        return


class BaseGallery(GalleryABC):
    """Directive to create a ``base-gallery`` with a toctree-like structure."""

    option_spec = {  # noqa: RUF012
        "tooltip": directives.flag,
        "caption": directives.unchanged,
    }
    has_content = True

    def run(self) -> list[nodes.Node]:
        """Generate the grid node for the base-gallery directive."""
        docname = self.env.docname
        src_dir = self.env.app.srcdir

        grid_node, row_node = create_grid_node(Grid(), self)
        for entry in self.content:
            if not entry:
                continue
            try:
                # Resolve the path relative to the current document
                entry_path = str(Path(self.env.relfn2path(entry.strip(), docname)[0]))
                entry_abs = Path(src_dir) / entry_path

                entry_files = parse_files_without_suffix(entry_abs)
                self.create_cards_for_row_node(
                    entry_files, row_node, save_thumbnail=True
                )
            except Exception as exc:
                msg = f"Error in directive '{self.name}' in document '{docname}': {exc}"
                logger.exception(msg)
                self.error(msg)
        grid_node += row_node
        return [grid_node, *self.create_toctree()]


class GalleryDirective(GalleryABC):
    """Directive to create a ``gallery`` with a toctree-like structure.

    .. hint::
        1. The items in this gallery are the files that contain the ``base-gallery``
           directives.
        2. The title of each file of items will be used as the section title in
           the gallery.
        3. The ``*`` wildcard can be used for matching multiple files.

    """

    option_spec = {  # noqa: RUF012
        "tooltip": directives.flag,
        "caption": directives.unchanged,
    }
    has_content = True

    def run(self) -> list[nodes.Node]:
        """Generate the grid and toctree nodes for the ``gallery`` directive."""
        docname = self.env.docname
        src_dir = self.env.app.srcdir

        section_nodes = []
        for entry in self.content:
            if not entry:
                continue

            try:
                # Resolve the path relative to the current document
                section_path = self.env.relfn2path(entry.strip(), docname)[0]
                section_abs = (Path(src_dir) / section_path).resolve()

                section_abs = list(section_abs.parent.glob(f"{section_abs.name}*"))[0]
                section_title, _ = extract_title_and_tooltip(section_abs)

                # title
                section_node = nodes.section()
                section_node["ids"] = [section_title]

                section_node += create_title_node(section_title)

                # grid
                grid_node, row_node = create_grid_node(Grid(), self)

                section_suffix = section_abs.suffix.lstrip(".")

                # cards
                card_files = get_base_gallery_items(
                    section_abs.open().read(), section_suffix
                )
                for card_file in card_files:
                    card_path = Path(
                        self.env.relfn2path(card_file.strip(), section_path)[0]
                    )
                    card_abs = Path(src_dir) / card_path
                    _cards_files = parse_files_without_suffix(card_abs)

                    self.create_cards_for_row_node(
                        _cards_files, row_node, save_thumbnail=False
                    )

                grid_node += row_node
                section_node += grid_node
                section_nodes.append(section_node)
            except Exception as exc:
                msg = f"Error in directive '{self.name}' in document '{docname}': {exc}"
                logger.exception(msg)
                self.error(msg)

        return section_nodes + self.create_toctree()


def ensure_config(
    config: GalleryConfig | GalleryThumbnailConfig | dict | None,
) -> GalleryConfig:
    """Ensure that the gallery config is set."""
    if isinstance(config, GalleryConfig):
        return config
    if isinstance(config, dict):
        return GalleryConfig(**config)
    if isinstance(config, GalleryThumbnailConfig):
        return GalleryConfig(**config.to_dict())
    if config is None:
        return GalleryConfig()  # use default config
    msg = (
        "The gallery config must be one of GalleryConfig, "
        f"GalleryThumbnailConfig, or a dict. But got {type(config)}"
    )
    raise TypeError(msg)


def format_option(option: dict) -> dict:
    """Format the option for the directive."""
    for key, value in option.items():
        if isinstance(value, list):
            option[key] = " ".join(value).split()
        else:
            option[key] = str(value)
    return option


def row_columns_option(argument: str | None) -> list[str]:
    """Validate the number of columns (out of 12) a grid row will have.

    One or four integers (for "xs sm md lg") between 1 and 12  (or 'auto').
    """
    return _media_option(argument, "sd-row-cols-", allow_auto=True)


def _media_option(
    argument: str | None,
    prefix: str,
    *,
    allow_auto: bool = False,
    min_num: int = 1,
    max_num: int = 12,
) -> list[str]:
    """Validate the number of columns (out of 12).

    One or four integers (for "xs sm md lg") between 1 and 12.
    """
    validate_error_msg = (
        "argument must be 1 or 4 (xs sm md lg) values, and each value should be "
        f"either 'auto' or an integer from {min_num} to {max_num}"
    )
    if argument is None:
        raise ValueError(validate_error_msg)
    values = argument.strip().split()
    if len(values) == 1:
        values = [values[0], values[0], values[0], values[0]]
    if len(values) != 4:
        raise ValueError(validate_error_msg)
    for value in values:
        if allow_auto and value == "auto":
            continue
        try:
            int_value = int(value)
        except Exception as exc:
            raise ValueError(validate_error_msg) from exc
        if not (min_num <= int_value <= max_num):
            raise ValueError(validate_error_msg)
    return [f"{prefix}{values[0]}"] + [
        f"{prefix}{size}-{value}"
        for size, value in zip(["xs", "sm", "md", "lg"], values)
    ]


class CardDirectiveWrapper(CardDirective):
    """A wrapper of the sphinx-design card directive to add gallery features.

    Modifications include:

    - Adding myst-sphinx-gallery classes to the card.
    - Adding loading="lazy" to the image tags.
    - Removing some unnecessary components.

    """

    @classmethod
    def create_card(
        cls,
        arguments: list,
        options: dict,
        sphinx_directive: SphinxDirective,
        offset: int = 0,
    ) -> nodes.Node:
        """Run the directive."""
        if sphinx_directive is not None:
            offset = sphinx_directive.content_offset
        card_classes = [
            "sd-card",
            "msg-sd-card",
            "sd-sphinx-override",
            "sd-text-center",
        ]
        if "width" in options:
            card_classes += [f'sd-w-{options["width"].rstrip("%")}']
        card_classes += options.get("margin", ["sd-mb-3"])
        card_classes += [f"sd-shadow-{options.get('shadow', 'lg')}"]
        if "link" in options:
            card_classes += ["sd-card-hover", "msg-sd-card-hover"]
        card = create_component(
            "card",
            card_classes
            + options.get("text-align", [])
            + options.get("class-card", []),
        )
        sphinx_directive.set_source_info(card)

        img_alt = options.get("img-alt") or ""

        container = card

        if "img-top" in options:
            image_top = nodes.image(
                "",
                uri=options["img-top"],
                alt=img_alt,
                classes=[
                    "sd-card-img-top",
                    "msg-sd-card-img-top",
                    *options.get("class-img-top", []),
                ],
                loading="lazy",
            )
            container.append(image_top)

        components = cls.split_content(sphinx_directive.content, offset)

        # Using a empty string list StringList() to avoid the write gallery content
        body = cls._create_component(
            sphinx_directive, "body", options, components.body[0], StringList()
        )
        if arguments:
            title = create_card_title_node(arguments[0], options, sphinx_directive)
            body.insert(0, title)
        container.append(body)

        if "link" in options:
            link_container = PassthroughTextElement()
            _classes = [
                "sd-stretched-link",
                "msg-sd-stretched-link",
                "sd-hide-link-text",
                "msg-sd-hide-link-text",
            ]
            _rawtext = options.get("link-alt") or options["link"]
            if options.get("link-type", "url") == "url":
                link = nodes.reference(
                    _rawtext,
                    "",
                    nodes.inline(_rawtext, _rawtext),
                    refuri=options["link"],
                    classes=_classes,
                )
            else:
                options = {
                    "classes": _classes,
                    "reftarget": options["link"],
                    "refdoc": sphinx_directive.env.docname,
                    "refdomain": "" if options["link-type"] == "any" else "std",
                    "reftype": options["link-type"],
                    "refexplicit": "link-alt" in options,
                    "refwarn": True,
                }
                link = addnodes.pending_xref(
                    _rawtext, nodes.inline(_rawtext, _rawtext), **options
                )
            sphinx_directive.set_source_info(link)
            link_container += link
            container.append(link_container)

        return card

    @classmethod
    def _create_component(
        cls,
        inst: SphinxDirective | None,
        name: str,
        options: dict,
        offset: int,
        content: StringList,
    ) -> nodes.container:
        """Create the header, body, or footer."""
        component = create_component(
            f"card-{name}", [f"sd-card-{name}", *options.get(f"class-{name}", [])]
        )
        cls.add_card_child_classes(component)
        if inst is not None:
            inst.set_source_info(component)
            inst.state.nested_parse(content, offset, component)
        return component


def create_grid_node(
    grid: Grid,
    sphinx_directive: SphinxDirective | None = None,
) -> tuple[nodes.Node, nodes.Node]:
    """Create a container node for the grid.

    Parameters
    ----------
    sphinx_directive : SphinxDirective
        The directive instance.
    grid : Grid
        The Grid instance which contains the grid options.

    Returns
    -------
    tuple[nodes.Node, nodes.Node]
        The grid and row nodes.

    """
    column_classes = []
    grid_classes = ["sd-container-fluid", "sd-sphinx-override", "msg-sd-container"]
    options = {key: list(val) for key, val in grid.class_options.items()}
    container = create_component(
        "grid-container",
        grid_classes
        + ["sd-mb-4"]
        + []
        + (["sd-border-1"] if "outline" in options else [])
        + options.get("class-container", []),
    )

    row = create_component(
        "grid-row",
        ["sd-row", "msg-sd-row"]
        + column_classes
        + options.get("gutter", [])
        + (["sd-flex-row-reverse"] if "reverse" in options else [])
        + options.get("class-row", []),
    )
    if sphinx_directive is not None:
        sphinx_directive.set_source_info(container)
        sphinx_directive.set_source_info(row)
    return container, row


def create_card_node(
    arguments: list,
    options: dict,
    sphinx_directive: SphinxDirective,
) -> nodes.Node:
    """Create a card node for the grid.

    Parameters
    ----------
    arguments : list
        The arguments for the card.
    options : dict
        The options for the card.
    sphinx_directive : SphinxDirective
        The directive instance.

    """
    column = create_component(
        "grid-item",
        [
            "sd-col",
            "msg-sd-col",
            "sd-d-flex-row",
            *options.get("columns", []),
            *options.get("margin", []),
            *options.get("padding", []),
            *options.get("class-item", []),
        ],
        node="card_col",
    )
    card_options = {
        key: value
        for key, value in options.items()
        if key
        in [
            "width",
            "text-align",
            "img-background",
            "img-top",
            "img-bottom",
            "img-alt",
            "link",
            "link-type",
            "link-alt",
            "shadow",
            "class-card",
            "class-body",
            "class-title",
            "class-header",
            "class-footer",
            "class-img-top",
            "class-img-bottom",
        ]
    }
    if "width" not in card_options:
        card_options["width"] = "100%"
    card_options["margin"] = []

    card = CardDirectiveWrapper.create_card(arguments, card_options, sphinx_directive)
    column += card
    return column


def create_title_node(title: str) -> nodes.Node:
    """Create a title node for the section."""
    pattern = r"``(.*?)``"  # rst pattern
    if "``" not in title:
        pattern = r"`(.*?)`"  # md pattern

    title_node = nodes.title()
    parts = re.split(pattern, title)
    matches = re.findall(pattern, title)

    for part in parts:
        if part:
            if part in matches:
                literal_node = nodes.literal()
                literal_node["classes"].append("docutils")
                literal_node["classes"].append("literal")
                literal_node["classes"].append("notranslate")
                literal_node += nodes.Text(part)
                title_node += literal_node
            else:
                title_node += nodes.Text(part)
    return title_node


def create_card_title_node(
    title: str,
    options: dict | None = None,
    sphinx_directive: SphinxDirective | None = None,
) -> nodes.Node:
    """Create a title node for the card.

    Parameters
    ----------
    title : str
        The title for the card.
    sphinx_directive : SphinxDirective
        The directive instance.
    options : dict, optional
        The options for the title node.

    """
    if options is None:
        options = {}
    title_node = create_component(
        "card-title",
        [
            "sd-card-title",
            "msg-sd-card-title",
            "sd-font-weight-bold",
            *options.get("class-title", []),
        ],
    )
    if sphinx_directive is not None:
        textnodes, _ = sphinx_directive.state.inline_text(
            title, sphinx_directive.lineno
        )
    else:
        textnodes = [
            nodes.reference(
                "", "", nodes.Text(title), refuri="", classes=["reference", "internal"]
            )
        ]

    title_container = PassthroughTextElement()
    title_container.extend(textnodes)
    title_node.append(title_container)
    if sphinx_directive is not None:
        sphinx_directive.set_source_info(title_container)
    return title_node


def create_component(
    name: str,
    classes: Sequence[str] = (),
    *,
    rawtext: str = "",
    children: Sequence[nodes.Node] = (),
    node: Literal["card_col"] | None = None,
    **attributes,
) -> nodes.container:
    """Create a container node for a design component."""
    node_class = {
        "card_col": card_col_node,
        "default": nodes.container,
    }
    if node is None:
        node = "default"

    node = node_class[node](
        rawtext, is_div=True, design_component=name, classes=list(classes), **attributes
    )
    node.extend(children)
    return node


class card_col_node(nodes.container):  # noqa: N801
    """A container node for a card column."""
