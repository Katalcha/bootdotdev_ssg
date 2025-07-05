from __future__ import annotations


class HTMLNode():
    def __init__(
        self,
        tag:                 str | None = None,
        value:               str | None = None,
        children: list[HTMLNode] | None = None,
        props:    dict[str, str | None] | None = None,
    ) -> None:
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self) -> str:
        raise NotImplementedError("Child class must override")

    def props_to_html(self) -> str:
        prop_str = ''
        if self.props:
            for key in self.props:
                prop_str += f' {key}="{self.props[key]}"'
        return prop_str

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag:   str | None,
        value: str,
        props: dict[str, str | None] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag:      str,
        children: list[HTMLNode],
        props:    dict[str, str | None] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")

        if self.children is None:
            raise ValueError("All parent nodes must have children nodes")

        children_html = ''
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
