import unittest
from htmlnode import HTMLNode


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

