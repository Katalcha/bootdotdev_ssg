import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        actual, expected = TextNode("This is a text node", TextType.BOLD), TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(actual, expected)

    def test_url_none_eq(self) -> None:
        actual, expected = TextNode("This is text", TextType.BOLD, None), TextNode("This is text", TextType.BOLD, None)
        self.assertEqual(actual, expected)

    def test_url_none_not_eq(self) -> None:
        actual, expected = TextNode("This is text", TextType.BOLD, None), TextNode("This is text", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(actual, expected)

    def test_text_not_eq(self) -> None:
        actual, expected = TextNode("This is a text node", TextType.BOLD), TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(actual, expected)

    def test_texttype_not_eq(self) -> None:
        actual, expected = TextNode("This is a text node", TextType.BOLD), TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(actual, expected)

    def test_repr(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        actual, expected = repr(node), "TextNode(This is a text node, text, https://www.boot.dev)"
        self.assertEqual(actual, expected)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        actual, expected = [html_node.tag, html_node.value], [None, "This is a text node"]
        self.assertListEqual(actual, expected)

    def test_bold(self) -> None:
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        actual, expected = [html_node.tag, html_node.value], ["b", "This is a bold text node"]
        self.assertListEqual(actual, expected)

    def test_italic(self) -> None:
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        actual, expected = [html_node.tag, html_node.value], ["i", "This is an italic text node"]
        self.assertListEqual(actual, expected)

    def test_code(self) -> None:
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        actual, expected = [html_node.tag, html_node.value], ["code", "This is a code block"]
        self.assertListEqual(actual, expected)

    def test_link(self) -> None:
        node = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        actual, expected = [html_node.tag, html_node.value, html_node.props], ["a", "This is a link", {"href": "https://boot.dev"}]
        self.assertListEqual(actual, expected)

    def test_image(self) -> None:
        node = TextNode("This is an image", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        actual, expected = [html_node.tag, html_node.value, html_node.props], ["img", "", {"src": "https://boot.dev", "alt": "This is an image"}]
        self.assertListEqual(actual, expected)

    def test_Error(self) -> None:
        node = TextNode("This is an invalid text node", "blockquote", "some_url") # type: ignore[reportArgumentType]
        node2 = TextNode("This is an invalid text node", None, None) # type: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
            text_node_to_html_node(node2)


if __name__ == "__main__":
    unittest.main()
