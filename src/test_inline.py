import unittest
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode



class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_with_code(self):
        # Simple code block delimiter
        text_type_text = "text"
        text_type_code = "code"

        node = TextNode("This is text with a `code block` word", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        assert result == [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

    def test_split_nodes_delimiter_with_bold(self):
        # Bold text delimiter
        text_type_text = "text"
        text_type_bold = "bold"

        node = TextNode("This is **bold** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        assert result == [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text),
        ]

    def test_split_nodes_delimiter_with_italic(self):
        # Italic text delimiter
        text_type_text = "text"
        text_type_italic = "italic"

        node = TextNode("This is *italic* text", text_type_text)
        result = split_nodes_delimiter([node], "*", text_type_italic)
        assert result == [
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text", text_type_text),
        ]

    def test_split_nodes_delimiter_with_unmatched_delimiter(self):
        # Unmatched delimiter (should raise an error)
        text_type_text = "text"
        text_type_code = "code"

        try:
            node = TextNode("This is unmatched `code block text", text_type_text)
            split_nodes_delimiter([node], "`", text_type_code)
        except ValueError as e:
            assert str(e) == "Unmatched delimiter '`' found in text: This is unmatched `code block text"

    def test_split_nodes_delimiter_with_no_delimiter(self):
        # No splitting needed (no delimiter present)
        text_type_text = "text"
        text_type_code = "code"

        node = TextNode("No delimiter here", text_type_text)
        result = split_nodes_delimiter([node], "`", text_type_code)
        assert result == [node]

    def test_split_nodes_delimiter_with_mixed_nodes(self):
        # Mixed nodes (only "text" nodes are split)
        text_type_text = "text"
        text_type_code = "code"
        text_type_bold = "bold"

        node1 = TextNode("Normal text", text_type_text)
        node2 = TextNode("**bold** text", text_type_bold)
        node3 = TextNode("Code `inline` text", text_type_text)
        result = split_nodes_delimiter([node1, node2, node3], "`", text_type_code)
        assert result == [
            node1,
            node2,
            TextNode("Code ", text_type_text),
            TextNode("inline", text_type_code),
            TextNode(" text", text_type_text),
        ]



class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        assert result == [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

    def test_extract_markdown_images_with_no_images(self):
        text = "This is text with no images"
        result = extract_markdown_images(text)
        assert result == []

    

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        assert result == [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    def test_extract_markdown_links_with_no_links(self):
        text = "This is text with no links"
        result = extract_markdown_links(text)
        assert result == []


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        text_type_text = "text"
        text_type_image = "image"

        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) image", text_type_text)
        result = split_nodes_image([node])
        assert result == [
            TextNode("This is text with a ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" image", text_type_text),
        ]

    def test_split_nodes_image_with_no_images(self):
        text_type_text = "text"

        node = TextNode("This is text with no images", text_type_text)
        result = split_nodes_image([node])
        assert result == [node]

    def test_split_nodes_image_with_mixed_nodes(self):
        text_type_text = "text"
        text_type_image = "image"

        node1 = TextNode("Normal text", text_type_text)
        node2 = TextNode("![](https://i.imgur.com/aKaOqIh.gif)", text_type_text)
        node3 = TextNode("Code `inline` text", text_type_text)
        result = split_nodes_image([node1, node2, node3])
        assert result == [
            node1,
            TextNode("", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            node3,
        ]


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        text_type_text = "text"
        text_type_link = "link"

        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", text_type_text)
        result = split_nodes_link([node])
        assert result == [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ]

    def test_split_nodes_link_with_no_links(self):
        text_type_text = "text"

        node = TextNode("This is text with no links", text_type_text)
        result = split_nodes_link([node])
        assert result == [node]

    def test_split_nodes_link_with_mixed_nodes(self):
        text_type_text = "text"
        text_type_link = "link"

        node1 = TextNode("Normal text", text_type_text)
        node2 = TextNode("[to boot dev](https://www.boot.dev)", text_type_text)
        node3 = TextNode("Code `inline` text", text_type_text)
        result = split_nodes_link([node1, node2, node3])
        assert result == [
            node1,
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            node3,
        ]


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_italic = "italic"
        text_type_code = "code"
        text_type_image = "image"
        text_type_link = "link"
        
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        assert result == [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            ]
        