import unittest
import os
from textnode import MarkdownBlockType, block_to_html, markdown_to_html

from textnode import TextNode, TextType, block_to_block_type, get_indexes, pair_indexes, split_blocks, split_by_md_syntax, split_nodes_img, split_nodes_link, text_node_to_html_node, split_nodes_delimeter, text_to_text_nodes, ParentNode

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

        tnode = TextNode("`this is code`", TextType.Code)
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = "<code>this is code</code>"
        self.assertEqual(node_html, target_html)

        tnode = TextNode("link", TextType.Link, url="https://www.google.com")
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<a href="https://www.google.com">link</a>'
        self.assertEqual(node_html, target_html)

        tnode = TextNode("alt text for image", TextType.Image, 'https://www.google.com')
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<img src="https://www.google.com" alt="alt text for image">'
        self.assertEqual(node_html, target_html)

    def test_texttype(self):
        tnode = TextNode("link", TextType.Link, url="https://www.google.com")
        hnode = text_node_to_html_node(tnode)
        node_html = hnode.to_html()
        target_html = '<a href="https://www.google.com">link</a>'
        self.assertEqual(node_html, target_html)


class TestIndexing(unittest.TestCase):
    def test_indexing(self):
        tnode = TextNode("This `is` text with a `code` block", TextType.Text)
        indices = get_indexes(text=tnode.text, delimeter='`')
        # pairs = pair_indexes(indexes, len(tnode.text))
        # split_text = split_by_md_syntax(tnode.text, pairs)
        split_text = split_by_md_syntax(tnode.text, indices)
        correct_text = ['This ', '`is`', ' text with a ', '`code`', ' block']
        self.assertEqual(split_text, correct_text)

        tnode = TextNode("This is **text** with a **bold** block", TextType.Text)
        indices = get_indexes(text=tnode.text, delimeter='**')
        split_text = split_by_md_syntax(tnode.text, indices)
        correct_text = ['This is ', '**text**',' with a ', '**bold**', ' block']
        self.assertEqual(split_text, correct_text)

        tnode = TextNode("This is *text* with an *italic* block", TextType.Text)
        indices = get_indexes(text=tnode.text, delimeter='*')
        split_text = split_by_md_syntax(tnode.text, indices)
        correct_text = ['This is ', '*text*',' with an ', '*italic*', ' block']
        self.assertEqual(split_text, correct_text)

class TestSplitting(unittest.TestCase):
    def test_split_delimeter(self):
        tnode = TextNode("This `is` text with a `code` block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], delimeter='`', text_type=TextType.Code)
        correct_nodes = [TextNode('This ', TextType.Text, None),
                         TextNode('is', TextType.Code, None),
                         TextNode(' text with a ', TextType.Text, None),
                         TextNode('code', TextType.Code, None),
                         TextNode(' block', TextType.Text, None)]

        self.assertEqual(new_nodes, correct_nodes)

        tnode = TextNode("This *is* text with an *italic* block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], delimeter='*', text_type=TextType.Italic)
        correct_nodes = [TextNode('This ', TextType.Text, None),
                         TextNode('is', TextType.Italic, None),
                         TextNode(' text with an ', TextType.Text, None),
                         TextNode('italic', TextType.Italic, None),
                         TextNode(' block', TextType.Text, None)]

        self.assertEqual(new_nodes, correct_nodes)

        tnode = TextNode("This **is** text with a **bold** block", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], delimeter='**', text_type=TextType.Bold)
        correct_nodes = [TextNode('This ', TextType.Text, None),
                         TextNode('is', TextType.Bold, None),
                         TextNode(' text with a ', TextType.Text, None),
                         TextNode('bold', TextType.Bold, None),
                         TextNode(' block', TextType.Text, None)]

        self.assertEqual(new_nodes, correct_nodes)

        tnode = TextNode("This *is* **text** with `mixed` types", TextType.Text)
        new_nodes = split_nodes_delimeter([tnode], delimeter='**', text_type=TextType.Bold)
        new_nodes = split_nodes_delimeter(new_nodes, delimeter='*', text_type=TextType.Italic)
        new_nodes = split_nodes_delimeter(new_nodes, delimeter='`', text_type=TextType.Code)
        correct_nodes = [TextNode('This ', TextType.Text, None),
                         TextNode('is', TextType.Italic, None),
                         TextNode(' ', TextType.Text, None),
                         TextNode('text', TextType.Bold, None),
                         TextNode(' with ', TextType.Text, None),
                         TextNode('mixed', TextType.Code, None),
                         TextNode(' types', TextType.Text, None)]
        self.assertEqual(new_nodes, correct_nodes)

    def test_split_img(self):
        node = TextNode("This is text with an ![image](https://www.google.com) and a ![second image](https://boot.dev) and with some text at the end", TextType.Text)
        new_nodes = split_nodes_img([node])
        correct_nodes = [TextNode('This is text with an ', TextType.Text, None),
                         TextNode('image', TextType.Image, "https://www.google.com"),
                         TextNode(' and a ', TextType.Text, None),
                         TextNode('second image', TextType.Image, "https://boot.dev"),
                         TextNode(' and with some text at the end', TextType.Text, None)]
        self.assertEqual(new_nodes, correct_nodes)
        # print(new_nodes)

    def test_split_link(self):
        node = TextNode("This is text with an [link](https://www.google.com) and a [second link](https://boot.dev) and with some text at the end", TextType.Text)
        second_node = TextNode("This has no links", TextType.Text)
        new_nodes = split_nodes_link([node, second_node])
        correct_nodes = [TextNode('This is text with an ', TextType.Text, None),
                         TextNode('link', TextType.Link, 'https://www.google.com'),
                         TextNode(' and a ', TextType.Text, None),
                         TextNode('second link', TextType.Link, 'https://boot.dev'),
                         TextNode(' and with some text at the end', TextType.Text, None),
                         TextNode('This has no links', TextType.Text)]
        # print(new_nodes)
        self.assertEqual(new_nodes, correct_nodes)

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        correct_nodes = [   TextNode("This is ", TextType.Text),
                            TextNode("text", TextType.Bold),
                            TextNode(" with an ", TextType.Text),
                            TextNode("italic", TextType.Italic),
                            TextNode(" word and a ", TextType.Text),
                            TextNode("code block", TextType.Code),
                            TextNode(" and an ", TextType.Text),
                            TextNode("obi wan image", TextType.Image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.Text),
                            TextNode("link", TextType.Link, "https://boot.dev"),
                        ]
        self.assertEqual(nodes, correct_nodes)

class TestSplittingBlocks(unittest.TestCase):
    def test_splitting_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = split_blocks(text)
        correct_blocks = [['# This is a heading'], ['This is a paragraph of text. It has some **bold** and *italic* words inside of it.'], ['* This is the first list item in a list block', '* This is a list item', '* This is another list item']]
        self.assertEqual(blocks, correct_blocks)

    def test_get_block_type(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is 
2. an
3. Ordered List

```
this is a code block
```

> this
> is
> a
> quote
"""
        blocks = split_blocks(text)
        blocks_typed = []
        for block in blocks:
            blocks_typed.append((block, block_to_block_type(block)))

        # expected = [(['# This is a heading'], <MarkdownBlockType.Heading: 1>), (['This is a paragraph of text. It has some **bold** and *italic* words inside of it.'], <MarkdownBlockType.Paragraph: 2>), (['* This is the first list item in a list block', '* This is a list item', '* This is another list item'], <MarkdownBlockType.Unordered_List: 5>), (['1. This is', '2. an', '3. Ordered List'], <MarkdownBlockType.Ordered_List: 6>), (['```', 'this is a code block', '```'], <MarkdownBlockType.Code: 3>), (['> this', '> is', '> a', '> quote'], <MarkdownBlockType.Quote: 4>)]
        expected = [(['# This is a heading'], MarkdownBlockType.Heading),
                    (['This is a paragraph of text. It has some **bold** and *italic* words inside of it.'], MarkdownBlockType.Paragraph),
                    (['* This is the first list item in a list block', '* This is a list item', '* This is another list item'], MarkdownBlockType.Unordered_List),
                    (['1. This is', '2. an', '3. Ordered List'], MarkdownBlockType.Ordered_List), (['```', 'this is a code block', '```'], MarkdownBlockType.Code),
                    (['> this', '> is', '> a', '> quote'], MarkdownBlockType.Quote)]
        self.assertEqual(blocks_typed, expected)

class TestFullMDToHTML(unittest.TestCase):
    def test_full_md_to_html(self):
        self.maxDiff = None
        dir_path = os.path.dirname(__file__)
        md_filepath = '../markdown/test_file.md'
        full_path = os.path.join(dir_path, md_filepath)
        with open(full_path, 'r') as f:
            markdown = f.read()
        final_html = markdown_to_html(markdown)
        

        expected_html = "<div><h1>An h1 header</h1><p>Paragraphs are separated by a blank line.</p><p>2nd paragraph.</p><p><i>Italic</i>, <b>bold</b>, and <code>monospace</code>. Itemized listslook like:</p><ul><li>this one</li><li>that one</li><li>the other one</li></ul><blockquote>Block quotes arewritten like so.They can span multiple paragraphs,if you like.</blockquote><h2>An h2 header</h2><p>Here's a numbered list:</p><ol><li>first item</li><li>second item</li><li>third item</li></ol><h3>An h3 header</h3><p>Code block:</p><pre><code>print('Hello world!')console.log('Hello world!')</code></pre><p>Here's a link to <a href=\"http://foo.bar\">a website</a></p><p>and images can be specified like so:<img src=\"example-image.jpg\" alt=\"example image\"></p></div>"
        

        self.assertEqual(final_html, expected_html)


if __name__ == "__main__":
    unittest.main()
