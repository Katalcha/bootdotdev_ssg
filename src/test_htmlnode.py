import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_result_eq(self):
        node = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')

    def test_props_to_html_eq(self):
        node = HTMLNode("p", "hello world", None, None)
        node2 = HTMLNode("p", "hello world", None, None)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_values(self):
        link = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        node = HTMLNode("div", "I wish I could read", [link], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, [link])
        self.assertEqual(node.props, {"class": "container"})

    def test_repr(self):
        inner = HTMLNode("a", "i am a link", None, {"href": "https://boot.dev", "target": "_blank"})
        outer = HTMLNode("p", "i am a paragraph", [inner], None)
        self.assertEqual("HTMLNode(p, i am a paragraph, children: [HTMLNode(a, i am a link, children: None, {'href': 'https://boot.dev', 'target': '_blank'})], None)", repr(outer))


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        expected = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_tag_not_eq(self):
        node = LeafNode("a", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), node2.to_html())

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "i am a link", {"href": "https://boot.dev", "target": "_blank"})
        expected = '<a href="https://boot.dev" target="_blank">i am a link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()
