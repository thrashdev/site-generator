import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimeter
import textnode

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
        tnode = TextNode("[link](https://www.google.com)", TextType.Link)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<a href="https://www.google.com">link</a>'
        self.assertEqual(node_html, target_html)

    def test_split_delimeter(self):
        tnode = TextNode("This is text with a **bold** block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], "**", TextType.Bold)
        expected = [TextNode('This', TextType.Text, None),
                    TextNode('is', TextType.Text, None),
                    TextNode('text', TextType.Text, None),
                    TextNode('with', TextType.Text, None),
                    TextNode('a', TextType.Text, None),
                    TextNode('bold', TextType.Bold, None),
                    TextNode('block', TextType.Text, None)]

        self.assertEqual(new_nodes, expected)

        tnode = TextNode("This is text with an *italic* block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], "*", TextType.Italic)
        expected = [TextNode('This', TextType.Text, None),
                    TextNode('is', TextType.Text, None),
                    TextNode('text', TextType.Text, None),
                    TextNode('with', TextType.Text, None),
                    TextNode('an', TextType.Text, None),
                    TextNode('italic', TextType.Italic, None),
                    TextNode('block', TextType.Text, None)]

        self.assertEqual(new_nodes, expected)
        
        tnode = TextNode("This is text with a `code` block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], '`', TextType.Code)
        expected = [TextNode('This', TextType.Text, None),
                    TextNode('is', TextType.Text, None),
                    TextNode('text', TextType.Text, None),
                    TextNode('with', TextType.Text, None),
                    TextNode('a', TextType.Text, None),
                    TextNode('code', TextType.Code, None),
                    TextNode('block', TextType.Text, None)]


        self.assertEqual(new_nodes, expected)
        tnode = TextNode("This *is* **mixed** text with a `code` block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], '`', TextType.Code)
        print("New nodes after code: " + str(new_nodes))
        new_nodes = split_nodes_delimeter(new_nodes, '*', TextType.Italic)
        print("New nodes after italic: " + str(new_nodes))
        new_nodes = split_nodes_delimeter(new_nodes, '**', TextType.Bold)
        print("New nodes after bold: " + str(new_nodes))


if __name__ == "__main__":
    unittest.main()
