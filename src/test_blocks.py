import unittest
from blocks import markdown_to_blocks, block_to_block_type



class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        
        result = markdown_to_blocks(markdown)

        assert result == [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]

    def test_markdown_to_blocks_with_empty_lines(self):
        markdown = "# This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        
        result = markdown_to_blocks(markdown)

        assert result == [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"

        result = block_to_block_type(block)

        assert result == "unordered_list"

    def test_block_to_block_type_with_heading(self):
        block = "# This is a heading"

        result = block_to_block_type(block)

        assert result == "heading"

    def test_block_to_block_type_with_unordered_list(self):
        block = "* This is a list item"

        result = block_to_block_type(block)

        assert result == "unordered_list"

    def test_block_to_block_type_with_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"

        result = block_to_block_type(block)

        assert result == "ordered_list"

    def test_block_to_block_type_with_code_block(self):
        block = "```This is a code block```"

        result = block_to_block_type(block)

        assert result == "code_block"

    def test_block_to_block_type_with_quote(self):
        block = "> This is a quote"

        result = block_to_block_type(block)

        assert result == "quote"

    def test_block_to_block_type_with_paragraph(self):
        block = "This is a paragraph of text"

        result = block_to_block_type(block)

        assert result == "paragraph"

    def test_block_to_block_type_with_invalid_ordered_list(self):
        block = "1. This is a list item\n1. This is another list item"

        result = block_to_block_type(block)

        assert result == "paragraph"

    def test_block_to_block_type_with_invalid_heading(self):
        block = "#This is a heading"

        result = block_to_block_type(block)

        assert result == "paragraph"

    def test_block_to_block_type_with_invalid_code_block(self):
        block = "```This is a code block"

        result = block_to_block_type(block)

        assert result == "paragraph"
