from typing import List
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
        delimeter_by_text_type = {TextType.Bold : '**', TextType.Code : '`', TextType.Italic : '*'}
        if text_type in delimeter_by_text_type:
            delimeter = delimeter_by_text_type[text_type]
            self.text = text.replace(delimeter, '')
        else:
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


def split_nodes_delimeter(old_nodes:List[TextNode], delimeter:str, text_type:TextType):
    text_type_by_delimeter = {"*" : TextType.Italic, "**" : TextType.Bold, '`' : TextType.Code}
    result:List[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            result.append(node)
            continue
        
        indices = get_indexes(node.text, delimeter)
        if len(indices) % 2 != 0:
            last_index = indices[-1]
            print(f"Unclosed markdown tag: {node.text[last_index:]} ")

        strings = split_by_md_syntax(node.text, indices)
        for s in strings:
            if delimeter in s:
                result.append(TextNode(s, text_type_by_delimeter[delimeter], None))
            else:
                result.append(TextNode(s, TextType.Text, None))
        # result.extend([TextNode(s, text_type_by_delimeter[delimeter], None) for s in strings])
    return result


def get_indexes(text, delimeter):
    patterns = {'**' : r'\*\*', '*' : r'\*', '`' : '`'}
    offsets = {'**' : 2, '*' : 1, '`' : 1}
    pat = patterns[delimeter]
    offset = offsets[delimeter]
    result = []
    for match in re.finditer(pat, text):
        start = match.start()
        end = match.start() + offset
        if len(result) % 2 == 0:
            result.append(start)
        else:
            result.append(end)
    result.insert(0,0)
    result.append(len(text))
    return result

def pair_indexes(indexes:list, text_length) -> list:
    result = []
    result.append((0, indexes[0]-1))
    last_index = indexes[-1]
    while indexes:
        result.append((indexes.pop(0)-1, indexes.pop(0)+1))
    result.append((last_index+1, text_length))
    return result

# def split_by_md_syntax(text, pairs:List[tuple]) -> List[str]:
#     result = []
#     for pair in pairs:
#         start = pair[0]
#         end = pair[1]
#         result.append(text[start:end])
#     return result

def split_by_md_syntax(text, indices:List[int]) -> List[str]:
    result = []
    for i in range (0, len(indices)):
        try:
            end = indices[i+1]
        except IndexError:
            break
        start = indices[i]
        s = text[start:end]
        result.append(s)
    return result
# def md_strip(text:str, pat) -> str:
#     value = map(lambda a: a.strip(pat), text.split(' '))
#     value = ' '.join(list(value))
#     return value
