from types import NotImplementedType

class HTMLTag():
    def __init__(self, tag) -> None:
        self.opening = f"<{tag}>"
        self.closing = f"</{tag}>"

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props:dict=None) -> None:
        self.tag = HTMLTag(tag)
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ""
        for k,v in self.props.items():
            html += f'{k}="{v}" '
        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props: dict = None) -> None:
        super().__init__(tag, value, None, props)
