import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href" : "https://www.google.com"}
        node = HTMLNode("a", "this is text of the paragraph", None, props )
        expected_props = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected_props)

class TestLeafNode(unittest.TestCase):
    def test_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text")
        target_html = "<p>This is a paragraph of text</p>"
        self.assertEqual(node.to_html(), target_html)


    def test_anchor(self):
        node = LeafNode("a", "Click me!", {"href" : "https://www.google.com"})
        target_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), target_html)
    
class TestParentNode(unittest.TestCase):
    def test_leaves_only(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )
        node_html = node.to_html()
        target_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node_html, target_html)
        
    def test_parent_in_parent(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    ParentNode("p", 
                               [ 
                            LeafNode("i", "italic text"),
                            LeafNode(None, "Normal text"),
                                ],)
                ],)

        target_html = "<p><b>Bold text</b><p><i>italic text</i>Normal text</p></p>"
        node_html = node.to_html()

        self.assertEqual(node_html, target_html)

if __name__ == '__main__':
    unittest.main()
