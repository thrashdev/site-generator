from typing import List, final
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

class MarkdownBlockType(Enum):
    Heading = 1
    Paragraph = 2
    Code = 3
    Quote = 4
    Unordered_List = 5
    Ordered_List = 6

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
        if not strings:
            result.append(node)
            continue
        for s in strings:
            if delimeter in s:
                result.append(TextNode(s, text_type_by_delimeter[delimeter], None))
            else:
                result.append(TextNode(s, TextType.Text, None))
        # result.extend([TextNode(s, text_type_by_delimeter[delimeter], None) for s in strings])
    return result

def split_nodes_img(old_nodes:List[TextNode]) -> List[TextNode]:
    pat_alt = r'\!\[(.*?)\]'
    pat_link = r"\((.*?)\)"
    result = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            result.append(node)
            continue
        indices_alt = []
        for match in re.finditer(pat_alt, node.text):
            start = match.start()
            end = match.end()
            indices_alt.append(start)

        indices_link = []
        for match in re.finditer(pat_link, node.text):
            start = match.start()
            end = match.end()
            indices_link.append(end)
        
        final_indices = []
        for i in range(0, len(indices_alt)):
            final_indices.append(indices_alt[i])
            final_indices.append(indices_link[i])

        if(len(final_indices)) % 2 != 0:
            raise RuntimeError(f"Unclosed tag: {node.text[final_indices[-1]:]}")
        # final_indices = list(zip(indices_alt, indices_link))
        final_indices.insert(0, 0)
        final_indices.append(len(node.text))
        for i in range (0,len(final_indices)):
            start = final_indices[i]
            try:
                end = final_indices[i+1]
            except IndexError:
                break
            s = node.text[start:end]
            full_img_pat = r'\!\[(.*?)\]\((.*?)\)'
            match = re.search(full_img_pat, s)
            if match:
                alt = match.group(1)
                link = match.group(2)
                result.append(TextNode(alt, TextType.Image, url=link))
            else:
                result.append(TextNode(s, TextType.Text))
        
    return result


def split_nodes_link(old_nodes:List[TextNode]) -> List[TextNode]:
    pat_alt = r'\[(.*?)\]'
    pat_link = r"\((.*?)\)"
    result = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            result.append(node)
            continue
        indices_alt = []
        for match in re.finditer(pat_alt, node.text):
            start = match.start()
            end = match.end()
            indices_alt.append(start)

        indices_link = []
        for match in re.finditer(pat_link, node.text):
            start = match.start()
            end = match.end()
            indices_link.append(end)
        
        final_indices = []
        for i in range(0, len(indices_alt)):
            final_indices.append(indices_alt[i])
            final_indices.append(indices_link[i])

        if(len(final_indices)) % 2 != 0:
            raise RuntimeError(f"Unclosed tag: {node.text[final_indices[-1]:]}")
        # final_indices = list(zip(indices_alt, indices_link))
        final_indices.insert(0, 0)
        final_indices.append(len(node.text))
        for i in range (0,len(final_indices)):
            start = final_indices[i]
            try:
                end = final_indices[i+1]
            except IndexError:
                break
            s = node.text[start:end]
            if s != '':
                full_img_link = r'\[(.*?)\]\((.*?)\)'
                match = re.search(full_img_link, s)
                if match:
                    alt = match.group(1)
                    link = match.group(2)
                    result.append(TextNode(alt, TextType.Link, url=link))
                else:
                    result.append(TextNode(s, TextType.Text))
        
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
    if len(result) > 0:
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

def text_to_text_nodes(text):
    result = []
    result = split_nodes_delimeter([TextNode(text, TextType.Text, None)], '**', TextType.Bold)
    result = split_nodes_delimeter(result, '*', TextType.Italic)
    result = split_nodes_delimeter(result, '`', TextType.Code)
    result = split_nodes_img(result)
    result = split_nodes_link(result)
    return result

def split_blocks(text):
        blocks = text.split('\n')
        blocks = list(map(str.strip, blocks))
        result = []
        temp = []
        for b in blocks:
            if b == '' or b == '\n':
                if temp != []: 
                    result.append(temp)
                temp = []
            else:
                temp.append(b)

        return result

def block_to_block_type(block:List[str]) -> MarkdownBlockType:
    available_tags = ['#', '*', '-', '>']
    tags_to_type = {'#' : MarkdownBlockType.Heading, '*' : MarkdownBlockType.Unordered_List, '-': MarkdownBlockType.Unordered_List, '>' : MarkdownBlockType.Quote }
    tags = [v[0] for v in block]
    tags = list(set(tags))

    first_line = block[0]
    if '# ' in first_line:
        count = first_line.count('#')
        if count in range (1,7):
            return MarkdownBlockType.Heading

    if all(ch == '`' for ch in block[0]) and all(ch == '`' for ch in block[-1]):
        return MarkdownBlockType.Code

    # if len(tags) == 1:
    #     tag = tags[0]
    #     if tag not in tags_to_type:
    #         return MarkdownBlockType.Paragraph
    #     return tags_to_type[tag]

    if len(tags) > 1:
        if not all(ch.isdigit() for ch in tags):
            return MarkdownBlockType.Paragraph

        for i, v in enumerate(tags):
            if (int(v) != (i+1)):
                return MarkdownBlockType.Paragraph
            
        return MarkdownBlockType.Ordered_List
    
    
    


# def md_strip(text:str, pat) -> str:
#     value = map(lambda a: a.strip(pat), text.split(' '))
#     value = ' '.join(list(value))
#     return value
