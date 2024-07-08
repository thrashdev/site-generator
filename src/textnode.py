from htmlnode import HTMLNode, LeafNode
from enum import Enum

class TextType(Enum):
    Text = 1
    Bold = 2
    Italic = 3
    Code = 4
    Link = 5
    Image = 6

class TextNode():
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
 
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.Text:
            return LeafNode(value=text_node.text)
        case TextType.Bold:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.Italic:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.Code:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.Link:
            return LeafNode(tag="a", value=text_node.text, props={"href" : text_node.url})
        case TextType.Image:
            return LeafNode(tag="img", value='', props={"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise ValueError("Submitted text node is not in the list of supported text types")
