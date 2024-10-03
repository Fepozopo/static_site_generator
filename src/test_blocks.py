import unittest
from blocks import *
from htmlnode import *



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


class TestMarkdownToHTML(unittest.TestCase):
    
    def test_text_to_children(self):
        result = text_to_children("This is **bold** and *italic*.")
        expected = [
            LeafNode(None, "This is ", None),
            LeafNode("b", "bold", None),
            LeafNode(None, " and ", None),
            LeafNode("i", "italic", None),
            LeafNode(None, ".", None)
        ]
        self.assertEqual(result, expected)

    def test_block_to_html_node_heading(self):
        block = "# Heading 1"
        result = block_to_html_node(block)
        expected = ParentNode("h1", [LeafNode(None, "Heading 1", None)])
        self.assertEqual(result, expected)

    def test_block_to_html_node_paragraph(self):
        block = "This is a paragraph."
        result = block_to_html_node(block)
        expected = ParentNode("p", [LeafNode(None, "This is a paragraph.", None)])
        self.assertEqual(result, expected)

    def test_block_to_html_node_unordered_list(self):
        block = "* Item 1\n* Item 2"
        result = block_to_html_node(block)
        expected = ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "Item 1", None)]),
            ParentNode("li", [LeafNode(None, "Item 2", None)])
        ])
        self.assertEqual(result, expected)

    def test_markdown_to_html_node(self):
        markdown = "# Title\n\nThis is a **bold** paragraph.\n\n* Item 1\n* Item 2"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Title", None)]),
            ParentNode("p", [
                LeafNode(None, "This is a ", None),
                LeafNode("b", "bold", None),
                LeafNode(None, " paragraph.", None)
            ]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1", None)]),
                ParentNode("li", [LeafNode(None, "Item 2", None)])
            ])
        ])
        self.assertEqual(result, expected)

    def test_markdown_to_html_node_with_whitespace(self):
        markdown = """
            # Heading 1

            This is a **bold** text and *italic* text.

            1. First item
            2. Second item

            > A blockquote.
        """
        result = markdown_to_html_node(markdown)

        expected = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading 1", None)]),
            ParentNode("p", [
                LeafNode(None, "This is a ", None),
                LeafNode("b", "bold", None),
                LeafNode(None, " text and ", None),
                LeafNode("i", "italic", None),
                LeafNode(None, " text.", None)
            ]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "First item", None)]),
                ParentNode("li", [LeafNode(None, "Second item", None)]),
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "A blockquote.", None)
            ])
        ])

        self.assertEqual(result, expected)