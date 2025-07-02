import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
