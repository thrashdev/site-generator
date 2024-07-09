from htmlnode import HTMLNode, LeafNode
from enum import Enum
import re

class TextType(Enum):
    Text = 1
    Bold = 2
    Italic = 3
    Code = 4
    Link = 5
    Image = 6

class TextNode():
    def __init__(self, text:str, text_type:TextType, url=None):
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
            md_bold = '**'
            value = text_node.text.strip(md_bold)
            return LeafNode(tag="b", value=value)
        case TextType.Italic:
            md_italic = '*'
            value = text_node.text.strip(md_italic)
            return LeafNode(tag="i", value=value)
        case TextType.Code:
            value = prep_inline_code(text_node.text)
            return LeafNode(tag="code", value=value)
        case TextType.Link:
            alt, link = prep_inline_link(text_node.text)
            return LeafNode(tag="a", value=alt, props={"href" : link})
        case TextType.Image:
            alt, link = prep_inline_img(text_node.text)
            return LeafNode(tag="img", value='', props={"src" : link, "alt" : alt})
        case _:
            raise ValueError("Submitted text node's text type is not in the list of supported text types")

def prep_inline_code(text):
    value = map(lambda a: a if '`' not in a else '', text.split('\n'))
    value = ''.join(list(value))
    return value

def prep_inline_link(text):
    alt_pat = r"\[(.*?)\]"
    alt = re.search(alt_pat, text).group(0).strip('[').strip(']')
    link_pat = r"\((.*?)\)"
    link = re.search(link_pat, text).group(0).strip('(').strip(')')
    return alt, link


def prep_inline_img(text):
    alt_pat = r"\[(.*?)\]"
    alt = re.search(alt_pat, text).group(0).strip('[').strip(']')
    link_pat = r"\((.*?)\)"
    link = re.search(link_pat, text).group(0).strip('(').strip(')')
    return alt, link
# def md_strip(text:str, pat) -> str:
#     value = map(lambda a: a.strip(pat), text.split(' '))
#     value = ' '.join(list(value))
#     return value
