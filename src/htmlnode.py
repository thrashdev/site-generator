from typing import List

class HTMLNode():
    def __init__(self, tag=None, value=None, children=[], props:dict={}) -> None:
        self.tag = tag
        self.value = value
        self.children:List[HTMLNode] = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ""
        if self.props == {}: return html
        if self.props is None: return html
        for k,v in self.props.items():
            html += f' {k}="{v}"'
        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value:str='', props: dict = {}) -> None:
        assert(value is not None)
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: dict = {}) -> None:
        assert(tag is not None)
        assert(children is not None)
        assert(children != {})
        super().__init__(tag=tag,  children=children, props=props)

    def to_html(self):
        opening_tag = f"<{self.tag}>"
        closing_tag = f"</{self.tag}>"
        children_html = ''
        for child in self.children:
            children_html += child.to_html()
        return opening_tag + children_html + closing_tag
