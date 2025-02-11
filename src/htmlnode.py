class HTMLNode:
    def __init__(
        self,
        tag =None,
        value=None,
        children=None,
        props=None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict | None = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " ".join([f"{k}='{v}'" for k, v in self.props.items()])

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict | None = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value is required for leaf nodes")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{' ' if self.props else ''}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict | None = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Tag is required for parent nodes")
        if not self.children:
            raise ValueError("Children are required for parent nodes")
        return (
            f"<{self.tag}{' ' if self.props else ''}{self.props_to_html()}>"
            f"{''.join([child.to_html() for child in self.children])}"
            f"</{self.tag}>"
        )
