from types import NotImplementedType


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props:dict=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
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
    def __init__(self, tag, value:str, props: dict = None) -> None:
        assert(value is not None)
        super().__init__(tag, value, None, props)

    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}> {self.value} </{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: dict = None) -> None:
        super().__init__(tag,  children, props)
