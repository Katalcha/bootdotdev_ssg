import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_result_eq(self) -> None:
        node = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        actual, expected = node.props_to_html(), ' href="https://boot.dev" target="_blank"'
        self.assertEqual(actual, expected)

    def test_props_to_html_eq(self) -> None:
        node, node2 = HTMLNode("p", "hello world", None, None), HTMLNode("p", "hello world", None, None)
        actual, expected = node.props_to_html(), node2.props_to_html()
        self.assertEqual(actual, expected)

    def test_values(self) -> None:
        link = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        node = HTMLNode("div", "I wish I could read", [link], {"class": "container"})
        actual, expected = [node.tag, node.value, node.children, node.props], ["div", "I wish I could read", [link], {"class": "container"}]
        self.assertListEqual(actual, expected)

    def test_repr(self) -> None:
        inner = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        outer = HTMLNode("p", "i am a paragraph", [inner], None)
        actual, expected = repr(outer), "HTMLNode(p, i am a paragraph, children: [HTMLNode(a, i am a link, children: None, {'href': 'https://boot.dev', 'target': '_blank'})], None)"
        self.assertEqual(actual, expected)

    def test_to_html_not_implemented_error(self) -> None:
        with self.assertRaises(NotImplementedError):
            HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"}).to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self) -> None:
        node = LeafNode("p", "Hello, world!")
        actual, expected = node.to_html(), "<p>Hello, world!</p>"
        self.assertEqual(actual, expected)

    def test_leaf_to_html_tag_not_eq(self) -> None:
        node, node2 = LeafNode("a", "Hello, world!"), LeafNode("p", "Hello, world!")
        actual, expected = node.to_html(), node2.to_html()
        self.assertNotEqual(actual, expected)

    def test_leaf_to_html_props(self) -> None:
        node = LeafNode("a", "i am a link", {"href": "https://boot.dev", "target": "_blank"})
        actual, expected = node.to_html(), '<a href="https://boot.dev" target="_blank">i am a link</a>'
        self.assertEqual(actual, expected)

    def test_leaf_to_html_no_tag(self) -> None:
        node = LeafNode(None, "Hello, world!")
        actual, expected = node.to_html(), "Hello, world!"
        self.assertEqual(actual, expected)

    def test_leaf_to_html_value_error(self) -> None:
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html() # type: ignore[reportArgumentType]

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self) -> None:
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        actual, expected = parent_node.to_html(), "<div><span>child</span></div>"
        self.assertEqual(actual, expected)

    def test_to_html_with_grandchildren(self) -> None:
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        actual, expected = parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(actual, expected)

    def test_to_html_many_children(self) -> None:
        a, b, c, d = LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")
        node = ParentNode("p", [a, b, c, d])
        actual, expected = node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(actual, expected)

    def test_headings(self) -> None:
        a, b, c, d = LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")
        node = ParentNode("h2", [a, b, c, d])
        actual, expected = node.to_html(), "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>"
        self.assertEqual(actual, expected)

    def test_to_html_tag_value_error(self) -> None:
        a, b, c, d = LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")
        with self.assertRaises(ValueError):
            ParentNode(None, [a, b, c, d]).to_html() # type: ignore[reportArgumentType]

    def test_to_html_children_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ParentNode("h2", None).to_html() # type: ignore[reportArgumentType]


if __name__ == "__main__":
    unittest.main()
