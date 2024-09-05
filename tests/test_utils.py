import re
from pathlib import Path

import nbformat
import pytest

from myst_sphinx_gallery.utils import (
    _extract_md_title_and_tooltip,
    _extract_rst_title_and_tooltip,
    _get_md_base_gallery_directives,
    _get_rst_base_gallery_directives,
    _is_rst_title_line,
    _parse_rst_title,
    abs_path,
    ensure_dir_exists,
    extract_title_and_tooltip,
    get_base_gallery_items,
    get_rst_title,
    parse_files_without_suffix,
    remove_special_chars,
    safe_remove_file,
)

cwd = Path(__file__).parent

data_dir = cwd / "data"
out_dir = cwd / "_build/thumbnails"


@pytest.fixture
def root_dir():
    return Path("/root")


class TestAbsPath:
    def test_abs_path_relative(self, root_dir):
        relative_path = "subdir/file.txt"
        expected = (root_dir / relative_path).resolve()
        assert abs_path(relative_path, root_dir) == expected

    def test_abs_path_absolute(self, root_dir):
        absolute_path = "/subdir/file.txt"
        expected = (root_dir / f".{absolute_path}").resolve()
        assert abs_path(absolute_path, root_dir) == expected

    def test_abs_path_different_root(self):
        relative_path = "subdir/file.txt"
        new_root_dir = Path("/new_root")
        expected = (new_root_dir / relative_path).resolve()
        assert abs_path(relative_path, new_root_dir) == expected

    def test_abs_path_special_characters(self, root_dir):
        special_path = "subdir/../file.txt"
        expected = (root_dir / special_path).resolve()
        assert abs_path(special_path, root_dir) == expected


class TestEnsureDirExists:
    def test_ensure_dir_exists(self):
        ensure_dir_exists(out_dir)
        assert out_dir.is_dir()

    def test_remove_and_create(self):
        if out_dir.exists():
            files = list(out_dir.glob("*"))
            for file in files:
                safe_remove_file(file)
                safe_remove_file(file)  # test removing non-existent file
            out_dir.rmdir()
        ensure_dir_exists(out_dir)
        assert out_dir.is_dir()


class TestParseFilesWithoutSuffix:
    def test_valid_path_with_files(self, tmp_path):
        # Create test files
        (tmp_path / "file.txt").touch()
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()

        path = tmp_path / "file"
        expected_files = [tmp_path / "file.txt"]

        assert sorted(parse_files_without_suffix(path)) == sorted(expected_files)

    def test_path_with_wildcard(self, tmp_path):
        # Create test files
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()

        path = tmp_path / "file*"
        expected_files = [tmp_path / "file1.txt", tmp_path / "file2.txt"]

        assert sorted(parse_files_without_suffix(path)) == sorted(expected_files)

    def test_folder_with_wildcard(self, tmp_path):
        # Create test files
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()
        (tmp_path / "other1.txt").touch()
        (tmp_path / "other2.txt").touch()

        path = tmp_path / "*"
        expected_files = [
            tmp_path / "file1.txt",
            tmp_path / "file2.txt",
            tmp_path / "other1.txt",
            tmp_path / "other2.txt",
        ]

        assert sorted(parse_files_without_suffix(path)) == sorted(expected_files)

    def test_path_with_no_matching_files(self, tmp_path):
        path = tmp_path / "nonexistent"

        with pytest.raises(
            FileNotFoundError,
            match=re.escape(f"No file found for nonexistent.* in {path.parent}"),
        ):
            parse_files_without_suffix(path)

    def test_invalid_path(self):
        path = Path("/invalid/path")

        with pytest.raises(
            FileNotFoundError,
            match=re.escape(
                f"Directory not found: {path.parent}. Please check the path."
            ),
        ):
            parse_files_without_suffix(path)


class TestRemoveSpecialChars:
    def test_alphanumeric(self):
        input_string = "abc123"
        expected = "abc123"
        assert remove_special_chars(input_string) == expected

    def test_special_characters(self):
        input_string = "a!b@c#1$2%3^"
        expected = "a!bc123"
        assert remove_special_chars(input_string) == expected

    def test_spaces(self):
        input_string = "a b c 1 2 3"
        expected = "a b c 1 2 3"
        assert remove_special_chars(input_string) == expected

    def test_mixed_characters(self):
        input_string = "a! b@ c# 1$ 2% 3^"
        expected = "a! b c 1 2 3"
        assert remove_special_chars(input_string) == expected

    def test_empty_string(self):
        input_string = ""
        expected = ""
        assert remove_special_chars(input_string) == expected

    def test_only_special_characters(self):
        input_string = "!@#$%^&*()"
        expected = "!"
        assert remove_special_chars(input_string) == expected


class TestGetRstTitle:
    def test_valid_rst_content_with_title(self):
        content = """
        Title
        =====

        Some content here.
        """
        expected_title = "Title"
        assert get_rst_title(content=content) == expected_title

        content = """
        Title
        -----

        Some content here.
        """
        expected_title = "Title"
        assert get_rst_title(content=content) == expected_title

    def test_valid_rst_content_without_title(self):
        content = """
        Some content here.
        """
        expected_title = ""
        assert get_rst_title(content=content) == expected_title

    def test_rst_content_with_multiple_titles(self):
        content = """
        ======
        Title1
        ======

        Some content here.

        Title2
        ------
        """
        expected_title = "Title1"
        assert get_rst_title(content=content) == expected_title

    def test_empty_rst_content(self):
        content = ""
        expected_title = ""
        assert get_rst_title(content=content) == expected_title

    def test_invalid_input(self):
        with pytest.raises(
            ValueError, match="Either file_path or content should be provided."
        ):
            get_rst_title()


class TestGetSubGalleryItems:
    def test_rst_with_base_gallery_items(self):
        content = """
        .. base-gallery::

            item1
            item2
            item3
            item4
        """
        expected = ["item1", "item2", "item3", "item4"]
        assert get_base_gallery_items(content) == expected

    def test_rst_with_no_base_gallery_items(self):
        content = """
        .. base-gallery::
        """
        expected = []
        assert get_base_gallery_items(content) == expected

    def test_rst_with_malformed_base_gallery_items(self):
        content = """
        .. base-gallery::

        item1/subitem1
        item2/subitem2
        """
        expected = []
        assert get_base_gallery_items(content) == expected

    def test_rst_with_multiple_base_gallery_directives(self):
        content = """
        .. base-gallery::

            item1/subitem1
            item2/subitem2

        some_text_here

        .. base-gallery::

            item3/subitem3
            item4/subitem4
        """
        print(get_base_gallery_items(content))
        expected = [
            "item1/subitem1",
            "item2/subitem2",
            "item3/subitem3",
            "item4/subitem4",
        ]
        assert get_base_gallery_items(content) == expected

    def test_rst_with_options(self):
        content = """
        .. base-gallery::
            :option0:
            :option1: value1
            :option2: value2
            :option3:

            item1/subitem1
            item2/subitem2
        some_text_here
        """
        expected = ["item1/subitem1", "item2/subitem2"]
        assert get_base_gallery_items(content) == expected

    def test_rst_with_options1(self):
        content = """
        .. base-gallery::
            :option0:
            :option1: value1
            :option2: value2
            :option3:

            item1
            item2
        some_text_here
        """
        expected = ["item1", "item2"]
        assert get_base_gallery_items(content) == expected

    def test_with_other_directive(self):
        content = """
        .. other_directive::

            item1/subitem1
            item2/subitem2

        some text here
        some more text

        .. base-gallery::

            item3/subitem3
            item4/subitem4
        some text here
        """
        expected = ["item3/subitem3", "item4/subitem4"]
        assert get_base_gallery_items(content) == expected

    def test_rst_complex_items(self):
        content = """
        .. base-gallery::
            :option0: value0
            :option1: value1
            :option2:

            item1
            item2

        some text here
        some more text

        .. other_directive::

            item1/subitem1
            item2/subitem2

        some text here
        some more text

        .. other_directive::
            :option0: value0
            :option1:

            .. base-gallery::

                item3/subitem3
                item4/subitem4
            some text here

        .. base-gallery::

            item5/subitem5/sub
            item6/subitem6/sub
        some text here
        """
        expected = [
            "item1",
            "item2",
            "item5/subitem5/sub",
            "item6/subitem6/sub",
        ]
        assert get_base_gallery_items(content) == expected

    def test_md_with_base_gallery_items(self):
        content = """
        ```{base-gallery}

        item1
        item2
        item3
        item4
        ```
        """
        expected = ["item1", "item2", "item3", "item4"]
        assert get_base_gallery_items(content, style="md") == expected

    def test_md_with_no_base_gallery_items(self):
        content = """
        ```{base-gallery}
        ```
        """
        expected = []
        assert get_base_gallery_items(content, style="md") == expected

    def test_md_with_malformed_base_gallery_items(self):
        content = """
        ````{base-gallery}
        item1/subitem1
        item2/subitem2
        ````
        """
        expected = []
        assert get_base_gallery_items(content, style="md") == expected

    def test_md_with_multiple_base_gallery_directives(self):
        content = """
        ```{base-gallery}
        item1/subitem1
        item2/subitem2
        ```

        some text here

        ```{base-gallery}
        item3/subitem3
        item4/subitem4
        ```
        """
        expected = [
            "item1/subitem1",
            "item2/subitem2",
            "item3/subitem3",
            "item4/subitem4",
        ]
        assert get_base_gallery_items(content, style="md") == expected

    def test_md_with_options(self):
        content = """
        ```{base-gallery}
        :option0:
        :option1: value1
        :option2: value2
        :option3:

        item1/subitem1
        item2/subitem2
        ```
        """
        expected = ["item1/subitem1", "item2/subitem2"]
        assert get_base_gallery_items(content, style="md") == expected


class Test_GetRstBaseGallerys:
    def test_single_base_gallery_directive(self):
        content = """
        .. base-gallery::

            item1
            item2
        """
        expected = [".. base-gallery::\n\n    item1\n    item2"]
        assert _get_rst_base_gallery_directives(content) == expected

    def test_multiple_base_gallery_directives(self):
        content = """
        .. base-gallery::

            item1
            item2

        some text here

        .. base-gallery::

            item3
            item4
        """
        expected = [
            ".. base-gallery::\n\n    item1\n    item2",
            ".. base-gallery::\n\n    item3\n    item4",
        ]
        assert _get_rst_base_gallery_directives(content) == expected

    def test_base_gallery_with_options(self):
        content = """
        .. base-gallery::
            :option1: value1
            :option2: value2

            item1
            item2
        """
        expected = [
            ".. base-gallery::\n    :option1: value1\n    :option2: value2\n\n    item1\n    item2"
        ]
        assert _get_rst_base_gallery_directives(content) == expected

    def test_base_gallery_with_mixed_content(self):
        content = """
        .. base-gallery::

            item1
            item2

        some text here

        .. other_directive::

            item3
            item4

        .. base-gallery::

            item5
            item6
        """
        expected = [
            ".. base-gallery::\n\n    item1\n    item2",
            ".. base-gallery::\n\n    item5\n    item6",
        ]
        assert _get_rst_base_gallery_directives(content) == expected

    def test_no_base_gallery_directives(self):
        content = """
        .. other_directive::

            item1
            item2

        some text here
        """
        expected = []
        assert _get_rst_base_gallery_directives(content) == expected

    def test_complex_case(self):
        content = """
        .. base-gallery::
            :option0: value0
            :option1: value1
            :option2:

            item1
            item2

        some text here
        some more text

        .. other_directive::

            item1/subitem1
            item2/subitem2

        some text here
        some more text

        .. other_directive::
            :option0: value0
            :option1:

            .. base-gallery::

                item3/subitem3
                item4/subitem4
            some text here

        .. base-gallery::

            item5/subitem5/sub
            item6/subitem6/sub
        some text here
        """
        expected = [
            ".. base-gallery::\n    :option0: value0\n    :option1: value1\n    :option2:\n\n    item1\n    item2",
            ".. base-gallery::\n\n    item5/subitem5/sub\n    item6/subitem6/sub",
        ]
        assert _get_rst_base_gallery_directives(content) == expected


class TestGetMdBaseGallerys:
    def test_single_base_gallery_directive(self):
        content = """
        ```{base-gallery}

        item1
        item2
        ```
        """
        expected = ["```{base-gallery}\n\nitem1\nitem2\n```"]
        assert _get_md_base_gallery_directives(content) == expected

    def test_multiple_base_gallery_directives(self):
        content = """
        ```{base-gallery}

        item1
        item2
        ```

        some text here

        ```{base-gallery}

        item3
        item4
        ```
        """
        expected = [
            "```{base-gallery}\n\nitem1\nitem2\n```",
            "```{base-gallery}\n\nitem3\nitem4\n```",
        ]
        assert _get_md_base_gallery_directives(content) == expected

    def test_base_gallery_with_options(self):
        content = """
        ```{base-gallery}
        :option1: value1
        :option2: value2

        item1
        item2
        ```
        """
        expected = [
            "```{base-gallery}\n:option1: value1\n:option2: value2\n\nitem1\nitem2\n```"
        ]
        assert _get_md_base_gallery_directives(content) == expected

    def test_base_gallery_with_mixed_content(self):
        content = """
        ```{base-gallery}

        item1
        item2
        ```

        some text here

        ```{other_directive}

        item3
        item4
        ```

        ```{base-gallery}

        item5
        item6
        ```
        """
        expected = [
            "```{base-gallery}\n\nitem1\nitem2\n```",
            "```{base-gallery}\n\nitem5\nitem6\n```",
        ]
        assert _get_md_base_gallery_directives(content) == expected

    def test_no_base_gallery_directives(self):
        content = """
        ```{other_directive}

        item1
        item2
        ```

        some text here
        """
        expected = []
        assert _get_md_base_gallery_directives(content) == expected

    def test_complex_case(self):
        content = """
        ```{base-gallery}
        :option0: value0
        :option1: value1
        :option2:

        item1
        item2
        ```

        some text here
        some more text

        ```{other_directive}

        item1/subitem1
        item2/subitem2
        ```

        some text here
        some more text

        ````{other_directive}
        :option0: value0
        :option1:

        ```{base-gallery}

        item3/subitem3
        item4/subitem4
        ```
        ````
        some text here

        ```{base-gallery}

        item5/subitem5/sub
        item6/subitem6/sub
        ```
        some text here
        """
        expected = [
            "```{base-gallery}\n:option0: value0\n:option1: value1\n:option2:\n\nitem1\nitem2\n```",
            "```{base-gallery}\n\nitem5/subitem5/sub\nitem6/subitem6/sub\n```",
        ]
        assert _get_md_base_gallery_directives(content) == expected

    def test_real_case(self):
        content = """
        ```{base-gallery}
        :tooltip:

        code
        markdown
        markdown alt
        ```

        `````{admonition} Code for the gallery
        :class: dropdown tip

        The code for this gallery is:

        ````{code-block} rst
        :caption: index.md

        ```{base-gallery}
        :tooltip:

        code
        markdown
        markdown alt
        ```
        ````
        `````
        """
        expected = ["```{base-gallery}\n:tooltip:\n\ncode\nmarkdown\nmarkdown alt\n```"]
        assert _get_md_base_gallery_directives(content) == expected


class TestExtractTitleAndTooltip:
    def test_extract_title_and_tooltip_rst(self, tmp_path):
        content = """
        Title
        =====

        This is the tooltip paragraph.
        """
        file_path = tmp_path / "test.rst"
        file_path.write_text(content, encoding="utf-8")
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert extract_title_and_tooltip(file_path) == (
            expected_title,
            expected_tooltip,
        )

    def test_extract_title_and_tooltip_md(self, tmp_path):
        content = """
        # Title

        This is the tooltip paragraph.
        """
        file_path = tmp_path / "test.md"
        file_path.write_text(content, encoding="utf-8")
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert extract_title_and_tooltip(file_path) == (
            expected_title,
            expected_tooltip,
        )

    def test_extract_title_and_tooltip_ipynb(self, tmp_path):
        nb = nbformat.v4.new_notebook()
        nb_md_cell = nbformat.v4.new_markdown_cell(
            "# Title\n\nThis is the tooltip paragraph."
        )
        nb.cells.append(nb_md_cell)
        file_path = tmp_path / "test.ipynb"
        with file_path.open("w") as f:
            nbformat.write(nb, f)

        with file_path.open("r") as f:
            print(f.read())

        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert extract_title_and_tooltip(file_path) == (
            expected_title,
            expected_tooltip,
        )

    def test_extract_title_and_tooltip_invalid_extension(self, tmp_path):
        file_path = tmp_path / "test.txt"
        file_path.write_text("Invalid content", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid file extension: .txt"):
            extract_title_and_tooltip(file_path)


class TestExtractMarkdownTitleAndTooltip:
    def test_title_and_tooltip(self):
        content = """
        # Title

        This is the tooltip paragraph.
        """
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert _extract_md_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_only_title(self):
        content = """
        # Title
        """
        expected_title = "Title"
        expected_tooltip = ""
        assert _extract_md_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_no_title(self):
        content = """
        This is the tooltip paragraph.
        """
        expected_title = ""
        expected_tooltip = ""
        assert _extract_md_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_empty_content(self):
        content = ""
        expected_title = ""
        expected_tooltip = ""
        assert _extract_md_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_multiple_paragraphs(self):
        content = """
        # Title

        This is the tooltip paragraph.

        This is another paragraph.
        """
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert _extract_md_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_target_before_title(self):
        content = """
        (heading-target)=

        # Title

        This is the tooltip paragraph.

        This is another paragraph.
        """
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert _extract_md_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )


class TestExtractRstTitleAndTooltip:
    def test_title_and_tooltip(self):
        content = """
        Title
        =====

        This is the tooltip paragraph.
        """
        expected = ("Title", "This is the tooltip paragraph.")
        title, tooltip = _extract_rst_title_and_tooltip(content)
        assert (title, tooltip) == expected

    def test_only_title(self):
        content = """
        Title
        -----
        """
        expected_title = "Title"
        expected_tooltip = ""
        assert _extract_rst_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_no_title(self):
        content = """
        This is the tooltip paragraph.
        """
        expected_title = ""
        expected_tooltip = ""
        assert _extract_rst_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_empty_content(self):
        content = ""
        expected_title = expected_title = ""

        expected_tooltip = ""
        assert _extract_rst_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_multiple_paragraphs(self):
        content = """
        =====
        Title
        =====

        This is the tooltip paragraph.

        This is another paragraph.
        """
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert _extract_rst_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )

    def test_target_before_title(self):
        content = """
        .. _heading-target:

        Title
        =====

        This is the tooltip paragraph.

        This is another paragraph.
        """
        expected_title = "Title"
        expected_tooltip = "This is the tooltip paragraph."
        assert _extract_rst_title_and_tooltip(content) == (
            expected_title,
            expected_tooltip,
        )


class TestIsRstTitleLine:
    def test_is_rst_title_line(self):
        assert _is_rst_title_line("=====")
        assert _is_rst_title_line("-----")
        assert _is_rst_title_line("=====  ")
        assert _is_rst_title_line("-----  ")

    def test_is_not_rst_title_line(self):
        assert not _is_rst_title_line("== ==")
        assert not _is_rst_title_line("-- --")
        assert not _is_rst_title_line("==--==")
        assert not _is_rst_title_line("    ")


class TestParseRstTitle:
    def test_parse_rst_title(self):
        lines = ["Title", "=====", "This is the tooltip paragraph."]
        expected_title = "Title"
        expected_title_lines = ["Title", "====="]
        assert _parse_rst_title(lines) == (expected_title, expected_title_lines)

    def test_parse_rst_title_no_tooltip(self):
        lines = ["Title", "====="]
        expected_title = "Title"
        expected_title_lines = ["Title", "====="]
        assert _parse_rst_title(lines) == (expected_title, expected_title_lines)

    def test_parse_rst_title_no_title(self):
        lines = ["This is the tooltip paragraph."]
        expected_title = ""
        expected_title_lines = []
        assert _parse_rst_title(lines) == (expected_title, expected_title_lines)

    def test_parse_rst_title_empty_lines(self):
        lines = []
        expected_title = ""
        expected_title_lines = []
        assert _parse_rst_title(lines) == (expected_title, expected_title_lines)
