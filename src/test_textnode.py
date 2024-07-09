import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node, node2)
    
    def test_md_to_html(self):
        tnode = TextNode("**bold**", TextType.Bold)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = "<b>bold</b>"
        self.assertEqual(node_html, target_html)
        
        tnode = TextNode("This is just text", TextType.Text)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = "This is just text"
        self.assertEqual(node_html, target_html)
        
        tnode = TextNode("*italic*", TextType.Italic)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = "<i>italic</i>"
        self.assertEqual(node_html, target_html)

        tnode = TextNode(
"""
``` 
this is code
```
""", TextType.Code)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = "<code>this is code</code>"
        self.assertEqual(node_html, target_html)

        tnode = TextNode("[link](https://www.google.com)", TextType.Link)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<a href="https://www.google.com">link</a>'
        self.assertEqual(node_html, target_html)

        tnode = TextNode("![alt text for image](https://www.google.com)", TextType.Image)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<img src="https://www.google.com" alt="alt text for image">'
        self.assertEqual(node_html, target_html)

    def test_texttype(self):
        tnode = TextNode("[link](https://www.google.com)", TextType.Bold)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<a href="https://www.google.com">link</a>'
        self.assertEqual(node_html, target_html)

if __name__ == "__main__":
    unittest.main()
