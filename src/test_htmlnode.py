import unittest
from htmlnode import HTMLNode, LeafNode


# Create some tests for the HTMLNode class
class TestHTMLNode(unittest.TestCase):
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

