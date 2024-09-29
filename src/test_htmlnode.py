import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode



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



if __name__ == "__main__":
    unittest.main()