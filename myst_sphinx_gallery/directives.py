from __future__ import annotations

import warnings
from pathlib import Path

from docutils import nodes
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.directives.other import TocTree
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from sphinx_design.cards import CardDirective
from sphinx_design.grids import GridDirective, GridItemCardDirective
from sphinx_design.shared import PassthroughTextElement, create_component

from .config import GalleryConfig
from .gallery import (
    ExampleConverter,
    GalleryGenerator,
    SectionGenerator,
    generate_gallery,
)
from .grid import Grid, GridItemCard
from .utils import abs_path, file_in_folder


class MiniGallery(SphinxDirective):
    """Directive to create a mini gallery grid."""

    option_spec = {
        "source_galleries": lambda value: value.split(),
        "config": str,
    }
    has_content = True

    @property
    def default_config_name(self) -> str:
        return "myst_sphinx_gallery_default"

    def run(self) -> list[nodes.Node]:
        """Generate the grid node for the mini gallery."""
        config_dict_all = self._parse_all_galleries_config()
        source_galleries = self.options.get("source_galleries")
        if source_galleries is None:
            config_used = {
                self.default_config_name: config_dict_all[self.default_config_name]
            }
        else:
            config_used = {
                key: config_dict_all[key]
                for key in self.options.get("source_galleries")
            }
        config_directive = self._parse_directive_config()

        grid = config_directive.grid.copy()
        grid_node = self.create_grid(grid, config_used)

        return [grid_node]

    def create_grid(self, grid: Grid, config_used: GalleryConfig) -> nodes.container:
        """Create a container node for the grid."""
        # arguments = grid.grid_args
        try:
            column_classes = []
        except ValueError as exc:
            raise self.error(f"Invalid directive argument: {exc}") from exc
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
        self.set_source_info(container)
        row = create_component(
            "grid-row",
            ["sd-row", "msg-sd-row"]
            + column_classes
            + options.get("gutter", [])
            + (["sd-flex-row-reverse"] if "reverse" in options else [])
            + options.get("class-row", []),
        )
        self.set_source_info(row)
        # each item in a row should be a column

        for file_path in self.content:
            grid_item_card = self._parse_card(config_used, file_path)
            options_card = grid_item_card.options_format.copy()
            options_card.update(
                {key: list(val) for key, val in grid_item_card.class_options.items()}
            )
            card_node = self.create_card(grid_item_card.items, options_card)
            row += card_node
        container += row
        return container

    def create_card(self, arguments: list, options: dict) -> nodes.container:
        """Create a card node for the grid."""
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

        card = CardDirectiveWrapper.create_card(self, arguments, card_options)
        column += card
        return column

    def _parse_card(
        self, config_list: list[GalleryConfig], file_path: str
    ) -> GridItemCard:
        """Parse the gallery card for the given file path."""
        examples_dirs = []
        if not Path(file_path).suffix:
            file_path += "*"

        for _, config in config_list.items():
            for i, examples_dir in enumerate(config.examples_dirs):
                examples_dirs.append(str(examples_dir))
                if file_in_folder(file_path, examples_dir):
                    conv = ExampleConverter(
                        abs_path(file_path, examples_dir, method="rglob"),
                        examples_dir,
                        config.gallery_dirs[i],
                        config=config,
                    )
                    conv._parse_thumb()
                    grid_item_card: GridItemCard = config.grid_item_card.copy()
                    grid_item_card.add_option("img-top", conv.gallery_thumb)
                    grid_item_card.add_option("link", conv.target_ref)
                    grid_item_card.add_option("link-type", "ref")
                    grid_item_card.add_item(f":ref:`{conv.target_ref}`")
                    return grid_item_card
        msg = (
            "mini_gallery directive error: "
            f"File {file_path} not found in any of the given source_galleries: {examples_dirs}"
            "please check the paths of file and source_galleries and try again."
        )
        raise FileNotFoundError(msg)

    def _parse_all_galleries_config(self) -> dict[str, GalleryConfig]:
        """Parse the gallery configs from the directive options or env variables."""
        config = self.env.config
        if not hasattr(config, "gallery_config_names"):
            if not hasattr(config, "myst_sphinx_gallery_config"):
                msg = (
                    "To use `mini_gallery` directive, "
                    "please set either `gallery_config_names` or  `myst_sphinx_gallery_config` in your conf.py file. "
                )
                raise ValueError(msg)
            config_dict = {
                self.default_config_name: ensure_config(
                    config.myst_sphinx_gallery_config
                )
            }
        else:
            if self.default_config_name in config.gallery_config_names:
                warnings.warn(
                    f"The gallery config name `{self.default_config_name} is reserved for the default gallery config."
                    "This config will be ignored.",
                    "Please use a different name for the gallery config.",
                    stacklevel=2,
                )
            config_dict = {
                key: ensure_config(val)
                for key, val in config.gallery_config_names.items()
            }
            config_dict.update(
                {
                    self.default_config_name: ensure_config(
                        config.myst_sphinx_gallery_config
                    )
                }
            )

        return config_dict

    def _parse_directive_config(self) -> GalleryConfig:
        """Parse the gallery config from the directive options."""
        config_dict_all = self._parse_all_galleries_config()
        config_name = self.options.get("config")
        if config_name is None:
            config_name = self.default_config_name
        config_used = config_dict_all.get(config_name)

        return config_used

    @property
    def gallery_example(self) -> None:
        """This is an example for the ``mini_gallery`` directive.

        .. _mini_gallery_example_code:

        Examples for ``mini_gallery`` directive
        ---------------------------------------

        .. mini_gallery::

            01-RST_order
            02-nb_order
            03-md_order
            plot_image_code
            last
            01-RST_order
            02-nb_order
            03-md_order
            plot_image_code
            last

        .. admonition:: Show the code
            :class: toggle

            Following is the code used for the ``mini_gallery`` directive in
            this example:

            .. code-block:: rst

                Examples for ``mini_gallery`` directive
                ---------------------------------------

                .. mini_gallery::

                    01-RST_order
                    02-nb_order
                    03-md_order
                    plot_image_code
                    last
                    01-RST_order
                    02-nb_order
                    03-md_order
                    plot_image_code
                    last
        """
        return None


def ensure_config(config: GalleryConfig | dict):
    """Ensure that the gallery config is set."""
    if isinstance(config, GalleryConfig):
        return config
    elif isinstance(config, dict):
        return GalleryConfig(**config)
    else:
        msg = "The gallery config must be either a GalleryConfig instance or a dictionary."
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
        f"{'either auto or ' if allow_auto else ''}an integer from {min_num} to {max_num}"
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
    @classmethod
    def create_card(
        cls, inst: SphinxDirective, arguments: list, options: dict
    ) -> nodes.Node:
        """Run the directive."""
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
        inst.set_source_info(card)

        img_alt = options.get("img-alt") or ""

        container = card
        if "img-background" in options:
            card.append(
                nodes.image(
                    uri=options["img-background"],
                    classes=["sd-card-img", "msg-sd-card-img"],
                    alt=img_alt,
                )
            )
            overlay = create_component(
                "card-overlay", ["sd-card-img-overlay", "msg-sd-card-img-overlay"]
            )
            inst.set_source_info(overlay)
            card += overlay
            container = overlay

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

        components = cls.split_content(inst.content, inst.content_offset)

        if components.header:
            container.append(
                cls._create_component(
                    inst, "header", options, components.header[0], components.header[1]
                )
            )
        # Using a empty string list StringList() to avoid the write gallery content
        body = cls._create_component(
            inst, "body", options, components.body[0], StringList()
        )
        if arguments:
            title = create_component(
                "card-title",
                [
                    "sd-card-title",
                    "msg-sd-card-title",
                    "sd-font-weight-bold",
                    *options.get("class-title", []),
                ],
            )
            textnodes, _ = inst.state.inline_text(arguments[0], inst.lineno)
            title_container = PassthroughTextElement()
            title_container.extend(textnodes)
            inst.set_source_info(title_container)
            title.append(title_container)
            body.insert(0, title)
        container.append(body)

        if components.footer:
            container.append(
                cls._create_component(
                    inst, "footer", options, components.footer[0], components.footer[1]
                )
            )

        if "img-bottom" in options:
            image_bottom = nodes.image(
                "",
                uri=options["img-bottom"],
                alt=img_alt,
                classes=[
                    "sd-card-img-bottom",
                    "msg-sd-card-img-bottom",
                    *options.get("class-img-bottom", []),
                ],
            )
            container.append(image_bottom)

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
                    # TODO the presence of classes raises an error if the link cannot be found
                    "classes": _classes,
                    "reftarget": options["link"],
                    "refdoc": inst.env.docname,
                    "refdomain": "" if options["link-type"] == "any" else "std",
                    "reftype": options["link-type"],
                    "refexplicit": "link-alt" in options,
                    "refwarn": True,
                }
                link = addnodes.pending_xref(
                    _rawtext, nodes.inline(_rawtext, _rawtext), **options
                )
            inst.set_source_info(link)
            link_container += link
            container.append(link_container)

        return card
