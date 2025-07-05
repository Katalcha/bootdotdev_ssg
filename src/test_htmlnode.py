import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_result_eq(self) -> None:
        node = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')

    def test_props_to_html_eq(self) -> None:
        node = HTMLNode("p", "hello world", None, None)
        node2 = HTMLNode("p", "hello world", None, None)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_values(self) -> None:
        link = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        node = HTMLNode("div", "I wish I could read", [link], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, [link])
        self.assertEqual(node.props, {"class": "container"})

    def test_repr(self) -> None:
        inner = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        outer = HTMLNode("p", "i am a paragraph", [inner], None)
        self.assertEqual("HTMLNode(p, i am a paragraph, children: [HTMLNode(a, i am a link, children: None, {'href': 'https://boot.dev', 'target': '_blank'})], None)", repr(outer))

    def test_to_html_not_implemented_error(self) -> None:
        node = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self) -> None:
        node = LeafNode("p", "Hello, world!")
        expected = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_tag_not_eq(self) -> None:
        node = LeafNode("a", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), node2.to_html())

    def test_leaf_to_html_props(self) -> None:
        node = LeafNode("a", "i am a link", {"href": "https://boot.dev", "target": "_blank"})
        expected = '<a href="https://boot.dev" target="_blank">i am a link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_no_tag(self) -> None:
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_value_error(self) -> None:
        node = LeafNode("p", None) # type: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self) -> None:
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self) -> None:
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_many_children(self) -> None:
        a = LeafNode("b", "Bold text")
        b = LeafNode(None, "Normal text")
        c = LeafNode("i", "italic text")
        d = LeafNode(None, "Normal text")
        node = ParentNode("p", [a, b, c, d])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_headings(self) -> None:
        a = LeafNode("b", "Bold text")
        b = LeafNode(None, "Normal text")
        c = LeafNode("i", "italic text")
        d = LeafNode(None, "Normal text")
        node = ParentNode("h2", [a, b, c, d])
        self.assertEqual(node.to_html(), "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>")

    def test_to_html_tag_value_error(self) -> None:
        a = LeafNode("b", "Bold text")
        b = LeafNode(None, "Normal text")
        c = LeafNode("i", "italic text")
        d = LeafNode(None, "Normal text")
        node = ParentNode(None, [a, b, c, d]) # type: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_children_value_error(self) -> None:
        node = ParentNode("h2", None) # type: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
