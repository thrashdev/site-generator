import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {}
        props["a"] = "www.google.com"
        node = HTMLNode("p", "this is text of the paragraph", None, props )
        expected_props = 'a = "www.google.com"'
        self.assertEqual(node.props_to_html(), expected_props)
