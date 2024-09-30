import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode



class TestHTMLNode(unittest.TestCase):
# Create some tests for the HTMLNode class
    def test_props_to_html_with_props(self):
        # Test with props
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.example.com", "target": "_blank"})
        expected_output = 'href="https://www.example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_no_props(self):
        # Test with no props
        node = HTMLNode(tag="p", value="No props here", props=None)
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    def test_repr(self):
        # Test __repr__ method
        children = [HTMLNode(tag="span", value="Child text")]
        node = HTMLNode(tag="div", value=None, children=children, props={"class": "container"})
        expected_output = "HTMLNode(div, None, [HTMLNode(span, Child text, None, None)], {'class': 'container'})"
        self.assertEqual(repr(node), expected_output)


class TestLeafNode(unittest.TestCase):
# Create some tests for the LeafNode class
    def test_LeafNode_to_html_with_props(self):
        # Test LeafNode.to_html method with props
        node = LeafNode(tag="a", value="Click here", props={"href": "https://www.example.com", "target": "_blank"})
        expected_output = '<a href="https://www.example.com" target="_blank">Click here</a>'
        self.assertEqual(node.to_html(), expected_output)

    def test_LeafNode_to_html_no_props(self):
        # Test LeafNode.to_html method with no props
        node = LeafNode(tag="p", value="No props here", props=None)
        expected_output = "<p>No props here</p>"
        self.assertEqual(node.to_html(), expected_output)

    def test_LeafNode_to_html_no_tag(self):
        # Test LeafNode.to_html method with no tag
        node = LeafNode(tag=None, value="No tag here", props=None)
        expected_output = "No tag here"
        self.assertEqual(node.to_html(), expected_output)

    def test_LeafNode_to_html_no_value(self):
        # Test LeafNode.to_html method with no value
        try:
            node = LeafNode(tag="p", value=None, props=None)
            node.to_html()
        except ValueError as e:
            assert str(e) == "The value of a leaf node cannot be None"


class TestParentNode(unittest.TestCase):
# Create some tests for the ParentNode class
    def test_parent_node_with_children_and_props(self):
        # Test with valid tag, children, and properties
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Hello", None),
                LeafNode("strong", "world", {"class": "highlight"}),
            ],
            {"id": "content"}
        )
        assert node.to_html() == '<div id="content"><span>Hello</span><strong class="highlight">world</strong></div>'

    def test_parent_node_with_nested_children_and_props(self):
        # Test with nested ParentNode
        nested_node = ParentNode(
            "section",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold", None),
                        LeafNode(None, " text", None),
                    ],
                ),
                LeafNode("i", "Italic", None),
            ],
        )
        assert nested_node.to_html() == '<section><p><b>Bold</b> text</p><i>Italic</i></section>'

    def test_parent_node_with_no_tag(self):
        # Test ValueError when no tag
        try:
            invalid_node = ParentNode(
                None,
                [LeafNode("b", "Bold text", None)]
            )
            invalid_node.to_html()
        except ValueError as e:
            assert str(e) == "The tag of a parent node cannot be None"

    def test_parent_node_with_no_children(self):
        # Test ValueError when no children
        try:
            invalid_node = ParentNode("div", [])
            invalid_node.to_html()
        except ValueError as e:
            assert str(e) == "The children of a parent node cannot be None or empty"


class Test_text_note_to_html_node(unittest.TestCase):
# Create some tests for the text_node_to_html_node function
    def test_text_note_to_html_node_with_text(self):
        # Test text_node_to_html_node with TextNode and text_type = "text"
        node = TextNode("This is a text node", "text")
        assert text_node_to_html_node(node) == LeafNode(None, "This is a text node", None)

    def test_text_note_to_html_node_with_bold(self):
        # Test text_node_to_html_node with TextNode and text_type = "bold"
        node = TextNode("This is a text node", "bold")
        assert text_node_to_html_node(node) == LeafNode("b", "This is a text node", None)

    def test_text_note_to_html_node_with_italic(self):
        # Test text_node_to_html_node with TextNode and text_type = "italic"
        node = TextNode("This is a text node", "italic")
        assert text_node_to_html_node(node) == LeafNode("i", "This is a text node", None)

    def test_text_note_to_html_node_with_code(self):
        # Test text_node_to_html_node with TextNode and text_type = "code"
        node = TextNode("This is a text node", "code")
        assert text_node_to_html_node(node) == LeafNode("code", "This is a text node", None)

    def test_text_note_to_html_node_with_link(self):
        # Test text_node_to_html_node with TextNode and text_type = "link"
        node = TextNode("This is a text node", "link", "https://www.boot.dev")
        assert text_node_to_html_node(node) == LeafNode("a", "This is a text node", {"href": "https://www.boot.dev"})

    def test_text_note_to_html_node_with_image(self):
        # Test text_node_to_html_node with TextNode and text_type = "image"
        node = TextNode("This is a text node", "image", "https://www.boot.dev")
        assert text_node_to_html_node(node) == LeafNode("img", "", {"src": "https://www.boot.dev", "alt": "This is a text node"})

    def test_text_note_to_html_node_with_invalid_text_type(self):
        # Test ValueError when text_type is invalid
        node = TextNode("This is a text node", "invalid")
        try:
            text_node_to_html_node(node)
        except ValueError as e:
            assert str(e) == "Invalid text type: invalid"




if __name__ == "__main__":
    unittest.main()